import threading, os, uuid
from django.http import FileResponse, Http404
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from backend.common.export import export_csv, export_xlsx
from .models import AsyncJob

# Map resource -> (Model, fields)
from backend.transportador.frota.models import Vehicle, Position
from backend.transportador.pneus.models import Tire, Application
from backend.transportador.estoque.models import StockMove
from backend.transportador.manutencao.models import WorkOrder, Teste

RESOURCES = {
    "frota.vehicles": (Vehicle, ["id","placa","modelo","km","motorista"]),
    "frota.positions": (Position, ["id","veiculo","posicao","medida"]),
    "pneus.tires": (Tire, ["id","codigo","medida","dot","status","posicao_atual"]),
    "pneus.applications": (Application, ["id","medida","eixos_aplicaveis","operacao"]),
    "estoque.moves": (StockMove, ["id","tipo","qtd","data","obs"]),
    "manut.os": (WorkOrder, ["id","tipo","status","veiculo","agendamento"]),
    "manut.tests": (Teste, ["id","os_id","torque_ok","pressao_ok","rodagem_ok","data"]),
}

def _run_export(job_id):
    job = AsyncJob.objects.get(pk=job_id)
    job.status = "running"; job.save(update_fields=["status"])
    try:
        Model, fields = RESOURCES[job.resource]
        qs = Model.objects.all()
        # naive filter application (exact match)
        params = job.params or {}
        if isinstance(params, dict):
            filterable = {k: v for k, v in params.items() if v not in ("", None)}
            if filterable:
                qs = qs.filter(**filterable)
        # export to file
        os.makedirs(settings.EXPORTS_DIR, exist_ok=True)
        ext = "xlsx" if job.fmt == "xlsx" else "csv"
        filename = f"export_{job.resource}_{uuid.uuid4().hex}.{ext}"
        fpath = os.path.join(settings.EXPORTS_DIR, filename)
        if ext == "xlsx":
            resp = export_xlsx(qs, fields, filename=filename)
            with open(fpath, "wb") as f: f.write(resp.content)
        else:
            resp = export_csv(qs, fields, filename=filename)
            with open(fpath, "wb") as f: f.write(resp.content)
        job.file_path = fpath; job.status = "done"; job.save(update_fields=["file_path","status"])
    except Exception as e:
        job.status = "error"; job.error = str(e); job.save(update_fields=["status","error"])

class ExportJobApi(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        resource = request.data.get("resource")
        fmt = request.data.get("format", "csv")
        params = request.data.get("params", {})
        if resource not in RESOURCES:
            return Response({"detail":"resource inválido","resources": list(RESOURCES.keys())}, status=400)
        job = AsyncJob.objects.create(kind="export", resource=resource, fmt=fmt, params=params, user=request.user)
        t = threading.Thread(target=_run_export, args=(job.id,), daemon=True)
        t.start()
        return Response({"id": job.id, "status": job.status})

class ExportJobStatusApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, job_id):
        try:
            job = AsyncJob.objects.get(pk=job_id)
        except AsyncJob.DoesNotExist:
            raise Http404()
        data = {"id": job.id, "status": job.status, "error": job.error, "download": f"/api/jobs/{job.id}/download/" if job.status=="done" else None}
        return Response(data)

class ExportJobDownloadApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, job_id):
        try:
            job = AsyncJob.objects.get(pk=job_id)
        except AsyncJob.DoesNotExist:
            raise Http404()
        if job.status != "done" or not job.file_path or not os.path.exists(job.file_path):
            return Response(status=status.HTTP_404_NOT_FOUND)
        return FileResponse(open(job.file_path, "rb"), as_attachment=True, filename=os.path.basename(job.file_path))
