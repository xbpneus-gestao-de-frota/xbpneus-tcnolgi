import { useState } from "react";
import api from "../../api/http";

export default function DesmontarPneuModal({ isOpen, onClose, onSuccess, pneu }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    motivo: "RODIZIO",
    km_veiculo: "",
    data_desmontagem: new Date().toISOString().slice(0, 16),
    observacoes: ""
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await api.post("/api/transportador/pneus/desmontar/", {
        pneu_id: pneu.id,
        motivo: form.motivo,
        km_veiculo: parseInt(form.km_veiculo),
        data_desmontagem: form.data_desmontagem,
        observacoes: form.observacoes || null
      });
      onSuccess?.();
      onClose();
    } catch (ex) {
      setError(ex.response?.data?.detail || "Falha ao desmontar pneu.");
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-2xl p-6 max-w-md w-full mx-4">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Desmontar Pneu</h2>
        {error && <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">{error}</div>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Pneu</label>
            <input type="text" value={`${pneu?.codigo} - ${pneu?.medida}`} disabled className="w-full px-4 py-2 rounded-lg border border-gray-300 bg-gray-100"/></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Motivo *</label>
            <select value={form.motivo} onChange={(e) => setForm({...form, motivo: e.target.value})} required className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="RODIZIO">Rodízio</option><option value="MANUTENCAO">Manutenção</option><option value="DESGASTE">Desgaste</option><option value="AVARIA">Avaria</option>
            </select></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">KM do Veículo *</label>
            <input type="number" value={form.km_veiculo} onChange={(e) => setForm({...form, km_veiculo: e.target.value})} required className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"/></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Data de Desmontagem</label>
            <input type="datetime-local" value={form.data_desmontagem} onChange={(e) => setForm({...form, data_desmontagem: e.target.value})} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"/></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Observações</label>
            <textarea value={form.observacoes} onChange={(e) => setForm({...form, observacoes: e.target.value})} rows="2" className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"/></div>
          <div className="flex gap-3 pt-4">
            <button type="submit" disabled={loading} className="flex-1 px-4 py-2 rounded-lg bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 text-white font-medium hover:opacity-90 disabled:opacity-50">{loading ? "Desmontando..." : "Desmontar Pneu"}</button>
            <button type="button" onClick={onClose} className="px-4 py-2 rounded-lg border border-gray-300 text-gray-700 font-medium hover:bg-gray-50">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  );
}
