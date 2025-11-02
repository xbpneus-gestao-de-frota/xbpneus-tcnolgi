
import { useEffect, useState } from "react";
import api from "../../api/http";
import { getEmpresaId } from "../../api/me";

export default function Reports(){
  const [med, setMed] = useState([]);
  const [custos, setCustos] = useState([]);
  const [giro, setGiro] = useState([]);
  const [custoPos, setCustoPos] = useState([]);
  const [err, setErr] = useState("");

  useEffect(()=>{ (async()=>{
    try{
      const empresa = await getEmpresaId();
      const qp = empresa?`?empresa_id=${empresa}`:"";
      setMed((await api.get(`/api/reports/pneus/medicoes_por_posicao/${qp}`)).data);
      setCustos((await api.get(`/api/reports/manutencao/custos_por_os/${qp}`)).data);
      setGiro((await api.get(`/api/reports/estoque/giro/${qp}`)).data);
      setCustoPos((await api.get(`/api/reports/manutencao/custos_por_posicao/${qp}`)).data);
    }catch(e){ setErr("Falha ao carregar relatórios."); }
  })() },[]);

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold">Relatórios</h2>
      {err && <div className="text-red-400">{err}</div>}

      <section>
        <h3 className="font-semibold mb-2">Medições (média) por Tipo de Posição</h3>
        <div className="overflow-auto rounded border border-white/10">
          <table className="w-full text-sm">
            <thead className="bg-white/10"><tr><th className="p-2">Posição</th><th className="p-2">Sulco médio (mm)</th><th className="p-2">Pressão média (psi)</th></tr></thead>
            <tbody>{med.map((r,i)=>(<tr key={i} className="odd:bg-white/5"><td className="p-2">{r.posicao_tipo||"-"}</td><td className="p-2">{r.sulco_avg||"-"}</td><td className="p-2">{r.pressao_avg||"-"}</td></tr>))}</tbody>
          </table>
        </div>
      </section>

      <section>
        <h3 className="font-semibold mb-2">Custos por OS</h3>
        <div className="overflow-auto rounded border border-white/10">
          <table className="w-full text-sm">
            <thead className="bg-white/10"><tr><th className="p-2">OS</th><th className="p-2">Total</th></tr></thead>
            <tbody>{custos.map((r,i)=>(<tr key={i} className="odd:bg-white/5"><td className="p-2">{r.os_id}</td><td className="p-2">{r.total}</td></tr>))}</tbody>
          </table>
        </div>
      </section>

      <section>
        <h3 className="font-semibold mb-2">Giro de Estoque (por tipo)</h3>
        <div className="overflow-auto rounded border border-white/10">
          <table className="w-full text-sm">
            <thead className="bg-white/10"><tr><th className="p-2">Tipo</th><th className="p-2">Qtd</th></tr></thead>
            <tbody>{giro.map((r,i)=>(<tr key={i} className="odd:bg-white/5"><td className="p-2">{r.tipo}</td><td className="p-2">{r.qtd}</td></tr>))}</tbody>
          </table>
        </div>
      </section>

      <section>
        <h3 className="font-semibold mb-2">Custos por eixo/posição</h3>
        <div className="overflow-auto rounded border border-white/10">
          <table className="w-full text-sm">
            <thead className="bg-white/10"><tr><th className="p-2">Placa</th><th className="p-2">Eixo</th><th className="p-2">Posição</th><th className="p-2">Total</th></tr></thead>
            <tbody>{custoPos.map((r,i)=>(<tr key={i} className="odd:bg-white/5"><td className="p-2">{r["posicao__veiculo__placa"]}</td><td className="p-2">{r["posicao__eixo"]}</td><td className="p-2">{r["posicao__posicao_tipo"]}</td><td className="p-2">{r.total}</td></tr>))}</tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
