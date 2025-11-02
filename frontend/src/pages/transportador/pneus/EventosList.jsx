import { useEffect, useState } from "react";
import api from "../../../api/http";
import { getEmpresaId } from "../../../api/me";
export default function EventosList(){
  const [rows, setRows] = useState([]), [err,setErr] = useState("");
  useEffect(()=>{ (async()=>{
    try{
      const empresa = await getEmpresaId();
      const { data } = await api.get(`/api/transportador/pneus/eventos/${empresa?`?empresa_id=${empresa}`:""}`);
      setRows(data);
    }catch(e){ setErr("Erro ao carregar eventos."); }
  })(); },[]);
  return (
    <div>
      <h2 className="text-xl font-bold mb-3">Eventos de Pneu</h2>
      {err && <div className="text-red-400 mb-2">{err}</div>}
      <div className="overflow-auto rounded border border-white/10">
        <table className="w-full text-sm">
          <thead className="bg-white/10"><tr><th className="p-2 text-left">ID</th><th className="p-2 text-left">Tipo</th><th className="p-2 text-left">Pneu</th><th className="p-2 text-left">Veículo</th><th className="p-2 text-left">Quando</th></tr></thead>
          <tbody>{Array.isArray(rows)&&rows.map(r=>(<tr key={r.id} className="odd:bg-white/5"><td className="p-2">{r.id}</td><td className="p-2">{r.tipo||"-"}</td><td className="p-2">{r.pneu||"-"}</td><td className="p-2">{r.veiculo||"-"}</td><td className="p-2">{r.criado_em||r.data||"-"}</td></tr>))}</tbody>
        </table>
      </div>
    </div>
  );
}
