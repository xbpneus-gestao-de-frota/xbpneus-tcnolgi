import { useState } from "react";
import api from "../../api/http";

export default function MedicaoModal({ isOpen, onClose, onSuccess, pneu }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    profundidade_sulco: "",
    pressao: "",
    temperatura: "",
    condicao_visual: "BOA",
    data_medicao: new Date().toISOString().slice(0, 16),
    observacoes: ""
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await api.post("/api/transportador/pneus/medicao/", {
        pneu_id: pneu.id,
        profundidade_sulco: parseFloat(form.profundidade_sulco),
        pressao: form.pressao ? parseFloat(form.pressao) : null,
        temperatura: form.temperatura ? parseFloat(form.temperatura) : null,
        condicao_visual: form.condicao_visual,
        data_medicao: form.data_medicao,
        observacoes: form.observacoes || null
      });
      onSuccess?.();
      onClose();
    } catch (ex) {
      setError(ex.response?.data?.detail || "Falha ao registrar medição.");
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-2xl p-6 max-w-md w-full mx-4">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Registrar Medição</h2>
        {error && <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">{error}</div>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Pneu</label>
            <input type="text" value={`${pneu?.codigo} - ${pneu?.medida}`} disabled className="w-full px-4 py-2 rounded-lg border border-gray-300 bg-gray-100"/></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Profundidade Sulco (mm) *</label>
            <input type="number" step="0.01" value={form.profundidade_sulco} onChange={(e) => setForm({...form, profundidade_sulco: e.target.value})} required placeholder="Ex: 8.5" className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"/></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Pressão (PSI)</label>
            <input type="number" step="0.1" value={form.pressao} onChange={(e) => setForm({...form, pressao: e.target.value})} placeholder="Ex: 110" className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"/></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Temperatura (°C)</label>
            <input type="number" step="0.1" value={form.temperatura} onChange={(e) => setForm({...form, temperatura: e.target.value})} placeholder="Ex: 65" className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"/></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Condição Visual</label>
            <select value={form.condicao_visual} onChange={(e) => setForm({...form, condicao_visual: e.target.value})} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="BOA">Boa</option><option value="REGULAR">Regular</option><option value="RUIM">Ruim</option>
            </select></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Data da Medição</label>
            <input type="datetime-local" value={form.data_medicao} onChange={(e) => setForm({...form, data_medicao: e.target.value})} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"/></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Observações</label>
            <textarea value={form.observacoes} onChange={(e) => setForm({...form, observacoes: e.target.value})} rows="2" className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"/></div>
          <div className="flex gap-3 pt-4">
            <button type="submit" disabled={loading} className="flex-1 px-4 py-2 rounded-lg bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 text-white font-medium hover:opacity-90 disabled:opacity-50">{loading ? "Salvando..." : "Salvar Medição"}</button>
            <button type="button" onClick={onClose} className="px-4 py-2 rounded-lg border border-gray-300 text-gray-700 font-medium hover:bg-gray-50">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  );
}
