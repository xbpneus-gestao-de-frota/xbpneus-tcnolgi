import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Save, X } from 'lucide-react';
import api from "../../../api/http";
import Loader from "../../../components/Loader";
import PageHeader from "../../../components/PageHeader";

export default function EmpresaForm() {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = Boolean(id);

  const [loading, setLoading] = useState(isEdit);
  const [saving, setSaving] = useState(false);
  const [formData, setFormData] = useState({
    nome: "",
    tipo: "transportador",
    cnpj: "",
    razao_social: "",
    nome_fantasia: "",
    inscricao_estadual: "",
    inscricao_municipal: "",
    cep: "",
    endereco: "",
    numero: "",
    complemento: "",
    bairro: "",
    cidade: "",
    estado: "",
    telefone: "",
    celular: "",
    email: "",
    site: "",
    ativa: true,
  });

  useEffect(() => {
    if (isEdit) {
      loadEmpresa();
    }
  }, [id]);

  const loadEmpresa = async () => {
    try {
      const response = await api.get(`/api/transportador/empresas/empresas/${id}/`);
      setFormData(response.data);
    } catch (error) {
      alert("Erro ao carregar empresa");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);

    try {
      if (isEdit) {
        await api.put(`/api/transportador/empresas/empresas/${id}/`, formData);
        alert("Empresa atualizada com sucesso!");
      } else {
        await api.post("/api/transportador/empresas/empresas/", formData);
        alert("Empresa criada com sucesso!");
      }
      navigate("/dashboard/empresas");
    } catch (error) {
      alert("Erro ao salvar empresa");
      console.error(error);
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <Loader />;

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <PageHeader
        title={isEdit ? "Editar Empresa" : "Nova Empresa"}
        subtitle={isEdit ? "Atualizar dados da empresa" : "Cadastrar nova empresa"}
      />

      <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow max-w-4xl">
        {/* Informações Básicas */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-4">Informações Básicas</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Nome *</label>
              <input
                type="text"
                name="nome"
                value={formData.nome}
                onChange={handleChange}
                required
                className="w-full border px-3 py-2 rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Tipo *</label>
              <select
                name="tipo"
                value={formData.tipo}
                onChange={handleChange}
                required
                className="w-full border px-3 py-2 rounded"
              >
                <option value="transportador">Transportador</option>
                <option value="revenda">Revenda</option>
                <option value="borracharia">Borracharia</option>
                <option value="recapagem">Recapagem</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">CNPJ *</label>
              <input
                type="text"
                name="cnpj"
                value={formData.cnpj}
                onChange={handleChange}
                required
                className="w-full border px-3 py-2 rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Razão Social</label>
              <input
                type="text"
                name="razao_social"
                value={formData.razao_social}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Nome Fantasia</label>
              <input
                type="text"
                name="nome_fantasia"
                value={formData.nome_fantasia}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
          </div>
        </div>

        {/* Inscrições */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-4">Inscrições</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Inscrição Estadual</label>
              <input
                type="text"
                name="inscricao_estadual"
                value={formData.inscricao_estadual}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Inscrição Municipal</label>
              <input
                type="text"
                name="inscricao_municipal"
                value={formData.inscricao_municipal}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
          </div>
        </div>

        {/* Endereço */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-4">Endereço</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">CEP</label>
              <input
                type="text"
                name="cep"
                value={formData.cep}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium mb-1">Endereço</label>
              <input
                type="text"
                name="endereco"
                value={formData.endereco}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Número</label>
              <input
                type="text"
                name="numero"
                value={formData.numero}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Complemento</label>
              <input
                type="text"
                name="complemento"
                value={formData.complemento}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Bairro</label>
              <input
                type="text"
                name="bairro"
                value={formData.bairro}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Cidade</label>
              <input
                type="text"
                name="cidade"
                value={formData.cidade}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Estado</label>
              <input
                type="text"
                name="estado"
                value={formData.estado}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
          </div>
        </div>

        {/* Contato */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-4">Contato</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Telefone</label>
              <input
                type="text"
                name="telefone"
                value={formData.telefone}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Celular</label>
              <input
                type="text"
                name="celular"
                value={formData.celular}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Site</label>
              <input
                type="text"
                name="site"
                value={formData.site}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
          </div>
        </div>

        {/* Status */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-4">Status</h3>
          <div className="flex items-center">
            <input
              type="checkbox"
              name="ativa"
              checked={formData.ativa}
              onChange={handleChange}
              className="mr-2"
            />
            <label className="text-sm font-medium">Ativa</label>
          </div>
        </div>

        <div className="flex justify-end space-x-4">
          <button
            type="button"
            onClick={() => navigate(-1)}
            className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Cancelar
          </button>
          <button
            type="submit"
            className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            disabled={saving}
          >
            {saving ? "Salvando..." : "Salvar Empresa"}
          </button>
        </div>
      </form>
    </div>
  );
}

