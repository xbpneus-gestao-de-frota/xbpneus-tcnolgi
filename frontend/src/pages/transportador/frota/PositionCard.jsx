import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../../../api/http";

export default function PositionCard(){
  const { id } = useParams();
  const [data, setData] = useState(null);
  const [err, setErr] = useState("");
  useEffect(()=>{ (async()=>{
    try { const { data } = await api.get(`/api/transportador/frota/posicoes/${id}/card/`); setData(data); }
    catch { setErr("Falha ao carregar posição"); }
  })() }, [id]);

  if(err) return <div className="text-red-400">{err}</div>;
  if(!data) return <div>Carregando...</div>;

  const url = `${location.origin}/transportador/frota/posicao/${id}`;
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold">Posição {data.position_id} — Veículo {data.veiculo}</h2>
        <Link to="/transportador/frota" className="underline text-sm">← Frota</Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="p-3 rounded border border-white/10">
          <div className="text-sm text-white/70">Eixo / Lado / Rodado</div>
          <div className="text-lg">{data.eixo} / {data.lado} / {data.rodado}</div>
          <div className="text-sm text-white/70 mt-2">Tipo</div>
          <div className="text-lg">{data.posicao_tipo}</div>
        </div>

        <div className="p-3 rounded border border-white/10">
          <div className="text-sm text-white/70">Pneu aplicado</div>
          {data.pneu ? (
            <div className="text-lg">#{data.pneu.id} — {data.pneu.numero_serie} ({data.pneu.status})</div>
          ) : <div className="text-lg">—</div>}
        </div>

        <div className="p-3 rounded border border-white/10">
          <div className="text-sm text-white/70 mb-1">QR da posição</div>
          <Qr url={url} />
          <div className="text-xs break-all mt-2">{url}</div>
        </div>
      </div>

      <div className="flex gap-2 flex-wrap">
        <button className="px-3 py-1 bg-white/10 rounded" onClick={async()=>{
          const psi = prompt('Pressão (psi):'); const sulco = prompt('Sulco (mm):');
          if(!psi && !sulco) return;
          if(!data.pneu?.id){ alert('Sem pneu aplicado.'); return; }
          await api.post('/api/transportador/pneus/medicoes/', { pneu: data.pneu.id, pressao_psi: psi?parseFloat(psi):null, profundidade_sulco_mm: sulco?parseFloat(sulco):null });
          alert('Medição registrada');
        }}>Registrar medição</button>

        <button className="px-3 py-1 bg-white/10 rounded" onClick={async()=>{
          const pneuId = prompt('ID do pneu para aplicar:');
          if(!pneuId) return;
          const v = await api.get(`/api/transportador/pneus/pneus/validate_compat?pneu_id=${pneuId}&posicao_id=${id}`);
          if(!v.data.ok){ alert('Movimentação inválida: '+(v.data.errors||[]).join('; ')); return; }
          await api.post(`/api/transportador/pneus/pneus/${pneuId}/aplicar/`, { posicao_id: id });
          location.reload();
        }}>Aplicar pneu</button>

        <button className="px-3 py-1 bg-white/10 rounded" onClick={async()=>{
          if(!data.pneu?.id){ alert('Sem pneu aplicado.'); return; }
          await api.post(`/api/transportador/pneus/pneus/${data.pneu.id}/remover/`, {});
          location.reload();
        }}>Remover pneu</button>
      </div>
    </div>
  );
}

function Qr({ url }){
  const [dataUrl, setDataUrl] = useState("");
  useEffect(()=>{ (async()=>{
    try{ const QR = (await import('qrcode')).default; const d = await QR.toDataURL(url); setDataUrl(d); }catch{ setDataUrl(""); }
  })() }, [url]);
  return dataUrl ? <img src={dataUrl} alt="QR" className="w-40 h-40 bg-white rounded p-1" /> : <div className="w-40 h-40 bg-white/10 rounded" />;
}
