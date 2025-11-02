import { useState } from "react";
import api from "../../api/http";
import { getEmpresaId } from "../../api/me";

export default function VeiculoForm({ onCreated }){
  const [form, setForm] = useState({ placa:"", categoria:"CAMINHAO", marca:"", modelo:"", ano:"", config_id:"" });
  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState("");

  const onChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  async function submit(e){
    e.preventDefault();
    setSaving(true); setErr("");
    try{
      const empresa = await getEmpresaId();
      const payload = { ...form, ano: form.ano?parseInt(form.ano):null, empresa };
      await api.post("/api/transportador/frota/veiculos/", payload);
      onCreated && onCreated();
      setForm({ placa:"", categoria:"CAMINHAO", marca:"", modelo:"", ano:"", config_id:"" });
    }catch(ex){ setErr("Falha ao criar veículo."); } finally { setSaving(false); }
  }

  return (
    <form onSubmit={submit} className="space-y-2">
      {err && <div className="text-red-400">{err}</div>}
      <div className="grid grid-cols-2 gap-2">
        <input className="bg-white/5 border border-white/10 rounded px-3 py-2" name="placa" placeholder="Placa" value={form.placa} onChange={onChange} required />
        <select className="bg-white/5 border border-white/10 rounded px-3 py-2" name="categoria" value={form.categoria} onChange={onChange}>
          <option value="CAMINHAO">Caminhão</option>
          <option value="ONIBUS">Ônibus</option>
          <option value="CARRETA">Carreta/Reboque</option>
          <option value="VAN">Van</option>
          <option value="OUTRO">Outro</option>
        </select>
        <input className="bg-white/5 border border-white/10 rounded px-3 py-2" name="marca" placeholder="Marca" value={form.marca} onChange={onChange} />
        <input className="bg-white/5 border border-white/10 rounded px-3 py-2" name="modelo" placeholder="Modelo" value={form.modelo} onChange={onChange} />
        <input className="bg-white/5 border border-white/10 rounded px-3 py-2" name="ano" placeholder="Ano" value={form.ano} onChange={onChange} />
        <input className="bg-white/5 border border-white/10 rounded px-3 py-2" name="config_id" placeholder="Config ID" value={form.config_id} onChange={onChange} />
      </div>
      <button disabled={saving} className="mt-2 px-4 py-2 rounded bg-green-600">{saving?"Salvando":"Salvar veículo"}</button>
    </form>
  );
}
