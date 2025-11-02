import { useState, useEffect } from "react";
import api from "../../api/http";

export default function MontarPneuModal({ isOpen, onClose, onSuccess, pneuId = null }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [veiculos, setVeiculos] = useState([]);
  const [pneus, setPneus] = useState([]);
  
  const [form, setForm] = useState({
    pneu_id: pneuId || "",
    veiculo_id: "",
    posicao: "",
    km_veiculo: "",
    data_montagem: new Date().toISOString().slice(0, 16),
    observacoes: ""
  });

  useEffect(() => {
    if (isOpen) {
      loadData();
    }
  }, [isOpen]);

  const loadData = async () => {
    try {
      const [veiculosRes, pneusRes] = await Promise.all([
        api.get("/api/transportador/frota/veiculos/"),
        api.get("/api/transportador/pneus/pneus/?status=ESTOQUE")
      ]);
      setVeiculos(veiculosRes.data.results || veiculosRes.data);
      setPneus(pneusRes.data.results || pneusRes.data);
    } catch (ex) {
      console.error("Erro ao carregar dados:", ex);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      await api.post("/api/transportador/pneus/montar/", {
        pneu_id: parseInt(form.pneu_id),
        veiculo_id: parseInt(form.veiculo_id),
        posicao: form.posicao,
        km_veiculo: parseInt(form.km_veiculo),
        data_montagem: form.data_montagem,
        observacoes: form.observacoes || null
      });
      
      onSuccess?.();
      onClose();
    } catch (ex) {
      setError(ex.response?.data?.detail || "Falha ao montar pneu.");
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-2xl p-6 max-w-md w-full mx-4">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Montar Pneu</h2>
        
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Pneu <span className="text-red-500">*</span>
            </label>
            <select
              value={form.pneu_id}
              onChange={(e) => setForm({...form, pneu_id: e.target.value})}
              required
              disabled={pneuId}
              className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
            >
              <option value="">Selecione um pneu</option>
              {pneus.map(p => (
                <option key={p.id} value={p.id}>{p.codigo} - {p.medida}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Veículo <span className="text-red-500">*</span>
            </label>
            <select
              value={form.veiculo_id}
              onChange={(e) => setForm({...form, veiculo_id: e.target.value})}
              required
              className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Selecione um veículo</option>
              {veiculos.map(v => (
                <option key={v.id} value={v.id}>{v.placa} - {v.modelo}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Posição <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={form.posicao}
              onChange={(e) => setForm({...form, posicao: e.target.value})}
              required
              placeholder="Ex: 1E, 1D, 2E, 2D..."
              className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              KM do Veículo <span className="text-red-500">*</span>
            </label>
            <input
              type="number"
              value={form.km_veiculo}
              onChange={(e) => setForm({...form, km_veiculo: e.target.value})}
              required
              className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Data de Montagem
            </label>
            <input
              type="datetime-local"
              value={form.data_montagem}
              onChange={(e) => setForm({...form, data_montagem: e.target.value})}
              className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Observações</label>
            <textarea
              value={form.observacoes}
              onChange={(e) => setForm({...form, observacoes: e.target.value})}
              rows="2"
              className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="flex gap-3 pt-4">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 px-4 py-2 rounded-lg bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 text-white font-medium hover:opacity-90 disabled:opacity-50"
            >
              {loading ? "Montando..." : "Montar Pneu"}
            </button>
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-lg border border-gray-300 text-gray-700 font-medium hover:bg-gray-50"
            >
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

