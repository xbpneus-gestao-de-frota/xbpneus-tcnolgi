import { useState } from "react";
import api from "../../api/http";
import { getEmpresaId } from "../../api/me";

export default function PneuForm({ onCreated }){
  const [form, setForm] = useState({ codigo:"", medida:"295/80R22.5", marca:"XBRI", linha:"", modelo:"", status:"ESTOQUE" });
  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState("");
  const onChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  async function submit(e){
    e.preventDefault();
    setSaving(true); setErr("");
    try{
      const empresa = await getEmpresaId();
      await api.post("/api/transportador/pneus/pneus/", { ...form, empresa });
      onCreated && onCreated();
      setForm({ codigo:"", medida:"295/80R22.5", marca:"XBRI", linha:"", modelo:"", status:"ESTOQUE" });
    }catch(ex){ setErr("Falha ao criar pneu."); } finally { setSaving(false); }
  }

  return (
    <form onSubmit={submit} className="space-y-2">
      {err && <div className="text-red-400">{err}</div>}
      <div className="grid grid-cols-2 gap-2">
        <input className="bg-white/5 border border-white/10 rounded px-3 py-2" name="codigo" placeholder="Código do pneu" value={form.codigo} onChange={onChange} required />
        <input className="bg-white/5 border border-white/10 rounded px-3 py-2" name="medida" placeholder="Medida (ex: 295/80R22.5)" value={form.medida} onChange={onChange} />
        <input className="bg-white/5 border border-white/10 rounded px-3 py-2" name="marca" placeholder="Marca" value={form.marca} onChange={onChange} />
        <input className="bg-white/5 border border-white/10 rounded px-3 py-2" name="linha" placeholder="Linha" value={form.linha} onChange={onChange} />
        <input className="bg-white/5 border border-white/10 rounded px-3 py-2" name="modelo" placeholder="Modelo" value={form.modelo} onChange={onChange} />
        <select className="bg-white/5 border border-white/10 rounded px-3 py-2" name="status" value={form.status} onChange={onChange}>
          <option value="ESTOQUE">Em estoque</option>
          <option value="APLICADO">Aplicado</option>
          <option value="GARANTIA">Em garantia</option>
          <option value="RECAPAGEM">Em recapagem</option>
          <option value="SUCATA">Sucata</option>
        </select>
      </div>
      <button disabled={saving} className="mt-2 px-4 py-2 rounded bg-green-600">{saving?"Salvando":"Salvar pneu"}</button>
    </form>
  );
}
