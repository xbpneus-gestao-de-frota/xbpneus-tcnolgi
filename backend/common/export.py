import csv, io
from django.http import StreamingHttpResponse, HttpResponse
from rest_framework.response import Response

def export_csv(queryset, fields, filename="export.csv"):
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(fields)
    for obj in queryset:
        row = []
        for f in fields:
            v = getattr(obj, f, "")
            if isinstance(v, bool):
                v = "1" if v else "0"
            row.append(v)
        writer.writerow(row)
    out = buf.getvalue().encode("utf-8")
    resp = HttpResponse(out, content_type="text/csv; charset=utf-8")
    resp["Content-Disposition"] = f'attachment; filename="{filename}"'
    return resp

def export_xlsx(queryset, fields, filename="export.xlsx"):
    try:
        from openpyxl import Workbook
    except Exception:
        # fallback: csv
        return export_csv(queryset, fields, filename=filename.replace(".xlsx",".csv"))
    wb = Workbook()
    ws = wb.active
    ws.append(fields)
    for obj in queryset:
        row = []
        for f in fields:
            v = getattr(obj, f, "")
            row.append(v)
        ws.append(row)
    out = io.BytesIO()
    wb.save(out)
    resp = HttpResponse(out.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    resp["Content-Disposition"] = f'attachment; filename="{filename}"'
    return resp


def export_csv_streaming(queryset, fields, filename="export.csv", chunk_size=1000):
    def row_iter():
        yield ",".join(fields) + "\n"
        for obj in queryset.iterator(chunk_size=chunk_size):
            vals = []
            for f in fields:
                v = getattr(obj, f, "")
                if isinstance(v, bool):
                    v = "1" if v else "0"
                s = str(v).replace('"','""')
                if any(c in s for c in [",", '"', "\n"]):
                    s = f'"{s}"'
                vals.append(s)
            yield ",".join(vals) + "\n"
    resp = StreamingHttpResponse(row_iter(), content_type="text/csv; charset=utf-8")
    resp["Content-Disposition"] = f'attachment; filename="{filename}"'
    return resp
