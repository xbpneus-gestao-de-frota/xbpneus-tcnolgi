import { useState } from "react";
import api from "../../api/http";
import { getEmpresaId } from "../../api/me";

export default function OSForm({ onCreated }){
  const [form, setForm] = useState({ veiculo:"", titulo:"", tipo:"CORRETIVA", prioridade:"MEDIA", status:"ABERTA" });
  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState("");
  const onChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  async function submit(e){
    e.preventDefault();
    setSaving(true); setErr("");
    try{
      const empresa = await getEmpresaId();
      await api.post("/api/transportador/manutencao/ordens/", { ...form, empresa });
      onCreated && onCreated();
      setForm({ veiculo:"", titulo:"", tipo:"CORRETIVA", prioridade:"MEDIA", status:"ABERTA" });
    }catch(ex){ setErr("Falha ao criar OS."); } finally { setSaving(false); }
  }

  return (
    <form onSubmit={submit} className="space-y-2">
      {err && <div className="text-red-400">{err}</div>}
      <div className="grid grid-cols-2 gap-2">
        <input className="bg-white/5 border border-white/10 rounded px-3 py-2" name="veiculo" placeholder="ID do veículo" value={form.veiculo} onChange={onChange} />
        <input className="bg-white/5 border border-white/10 rounded px-3 py-2" name="titulo" placeholder="Título" value={form.titulo} onChange={onChange} />
        <select className="bg-white/5 border border-white/10 rounded px-3 py-2" name="tipo" value={form.tipo} onChange={onChange}>
          <option value="PREVENTIVA">Preventiva</option>
          <option value="CORRETIVA">Corretiva</option>
        </select>
        <select className="bg-white/5 border border-white/10 rounded px-3 py-2" name="prioridade" value={form.prioridade} onChange={onChange}>
          <option value="BAIXA">Baixa</option>
          <option value="MEDIA">Média</option>
          <option value="ALTA">Alta</option>
          <option value="CRITICA">Crítica</option>
        </select>
        <select className="bg-white/5 border border-white/10 rounded px-3 py-2" name="status" value={form.status} onChange={onChange}>
          <option value="ABERTA">Aberta</option>
          <option value="EXECUCAO">Em execução</option>
          <option value="AGUARDANDO_PECA">Aguardando peça</option>
          <option value="FINALIZADA">Finalizada</option>
          <option value="CANCELADA">Cancelada</option>
        </select>
      </div>
      <button disabled={saving} className="mt-2 px-4 py-2 rounded bg-green-600">{saving?"Salvando":"Abrir OS"}</button>
    </form>
  );
}
