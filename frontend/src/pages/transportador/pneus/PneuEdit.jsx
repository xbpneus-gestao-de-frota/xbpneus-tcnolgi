import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../../../api/http";
import PageHeader from "../../../components/PageHeader";
import Loader from "../../../components/Loader";
import ErrorState from "../../../components/ErrorState";

export default function PneuEdit() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [saveError, setSaveError] = useState("");
  
  const [form, setForm] = useState({
    codigo: "", numero_fogo: "", medida: "", marca: "", modelo: "", tipo: "NOVO",
    dot: "", ano_fabricacao: "", semana_fabricacao: "", status: "ESTOQUE",
    posicao_atual: "", km_total: "0", km_atual: "0", profundidade_sulco: "",
    numero_recapagens: "0", pode_recapar: true, valor_compra: "", valor_atual: "",
    data_aquisicao: "", observacoes: ""
  });

  useEffect(() => { loadPneu(); }, [id]);

  const loadPneu = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/api/transportador/pneus/pneus/${id}/`);
      const data = response.data;
      setForm({
        codigo: data.codigo || "", numero_fogo: data.numero_fogo || "", medida: data.medida || "",
        marca: data.marca || "", modelo: data.modelo || "", tipo: data.tipo || "NOVO",
        dot: data.dot || "", ano_fabricacao: data.ano_fabricacao || "", semana_fabricacao: data.semana_fabricacao || "",
        status: data.status || "ESTOQUE", posicao_atual: data.posicao_atual || "",
        km_total: data.km_total || "0", km_atual: data.km_atual || "0",
        profundidade_sulco: data.profundidade_sulco || "", numero_recapagens: data.numero_recapagens || "0",
        pode_recapar: data.pode_recapar !== undefined ? data.pode_recapar : true,
        valor_compra: data.valor_compra || "", valor_atual: data.valor_atual || "",
        data_aquisicao: data.data_aquisicao || "", observacoes: data.observacoes || ""
      });
    } catch (ex) {
      setError("Falha ao carregar dados do pneu.");
    } finally {
      setLoading(false);
    }
  };

  const onChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setForm({ ...form, [e.target.name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setSaveError("");
    try {
      const payload = {
        codigo: form.codigo, numero_fogo: form.numero_fogo || null, medida: form.medida,
        marca: form.marca || null, modelo: form.modelo || null, tipo: form.tipo,
        dot: form.dot || "", ano_fabricacao: form.ano_fabricacao ? parseInt(form.ano_fabricacao) : null,
        semana_fabricacao: form.semana_fabricacao ? parseInt(form.semana_fabricacao) : null,
        status: form.status, posicao_atual: form.posicao_atual || "",
        km_total: parseInt(form.km_total) || 0, km_atual: parseInt(form.km_atual) || 0,
        profundidade_sulco: form.profundidade_sulco ? parseFloat(form.profundidade_sulco) : null,
        numero_recapagens: parseInt(form.numero_recapagens) || 0, pode_recapar: form.pode_recapar,
        valor_compra: form.valor_compra ? parseFloat(form.valor_compra) : 0,
        valor_atual: form.valor_atual ? parseFloat(form.valor_atual) : 0,
        data_aquisicao: form.data_aquisicao || null, observacoes: form.observacoes || null
      };
      await api.put(`/api/transportador/pneus/pneus/${id}/`, payload);
      navigate("/dashboard/pneus/lista");
    } catch (ex) {
      setSaveError("Falha ao atualizar pneu.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <Loader />;
  if (error) return <ErrorState message={error} />;

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <PageHeader title="Editar Pneu" subtitle={`Editando pneu ${form.codigo}`} />
      <div className="bg-white rounded-xl shadow-md p-6 max-w-4xl">
        {saveError && <div className="mb-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">{saveError}</div>}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Identificação</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Código *</label>
                <input type="text" name="codigo" value={form.codigo} onChange={onChange} required className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500" /></div>
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Número de Fogo</label>
                <input type="text" name="numero_fogo" value={form.numero_fogo} onChange={onChange} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500" /></div>
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Medida *</label>
                <input type="text" name="medida" value={form.medida} onChange={onChange} required className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500" /></div>
            </div>
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Especificações</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Marca</label>
                <input type="text" name="marca" value={form.marca} onChange={onChange} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500" /></div>
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Modelo</label>
                <input type="text" name="modelo" value={form.modelo} onChange={onChange} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500" /></div>
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Tipo</label>
                <select name="tipo" value={form.tipo} onChange={onChange} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option value="NOVO">Novo</option><option value="RECAPADO">Recapado</option><option value="REFORMADO">Reformado</option>
                </select></div>
            </div>
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Status</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                <select name="status" value={form.status} onChange={onChange} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option value="ESTOQUE">Em Estoque</option><option value="MONTADO">Montado</option><option value="MANUTENCAO">Em Manutenção</option>
                  <option value="SUCATA">Sucata</option><option value="RECAPAGEM">Em Recapagem</option><option value="VENDIDO">Vendido</option>
                </select></div>
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Profundidade Sulco (mm)</label>
                <input type="number" step="0.01" name="profundidade_sulco" value={form.profundidade_sulco} onChange={onChange} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500" /></div>
            </div>
          </div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Observações</label>
            <textarea name="observacoes" value={form.observacoes} onChange={onChange} rows="3" className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500" /></div>
          <div className="flex items-center gap-3 pt-4 border-t">
            <button type="submit" disabled={saving} className="px-6 py-2 rounded-lg bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 text-white font-medium hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed">
              {saving ? "Salvando..." : "Salvar Alterações"}</button>
            <button type="button" onClick={() => navigate("/dashboard/pneus/lista")} className="px-6 py-2 rounded-lg border border-gray-300 text-gray-700 font-medium hover:bg-gray-50 transition-colors">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  );
}
