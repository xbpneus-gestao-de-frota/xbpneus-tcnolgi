import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import useTryFetch from "../../../hooks/useTryFetch";
import api from "../../../api/http";
import Loader from "../../../components/Loader";
import PageHeader from "../../../components/PageHeader";

export default function FilialForm() {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = Boolean(id);

  const [loading, setLoading] = useState(isEdit);
  const [saving, setSaving] = useState(false);
  const [formData, setFormData] = useState({
    empresa: "",
    codigo: "",
    nome: "",
    cnpj: "",
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
    matriz: false,
    ativa: true,
  });

  // Buscar lista de empresas
  const { data: empresas } = useTryFetch(["/api/transportador/empresas/empresas/"]);

  useEffect(() => {
    if (isEdit) {
      loadFilial();
    }
  }, [id]);

  const loadFilial = async () => {
    try {
      const response = await api.get(`/api/transportador/empresas/filiais/${id}/`);
      setFormData(response.data);
    } catch (error) {
      alert("Erro ao carregar filial");
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
        await api.put(`/api/transportador/empresas/filiais/${id}/`, formData);
        alert("Filial atualizada com sucesso!");
      } else {
        await api.post("/api/transportador/empresas/filiais/", formData);
        alert("Filial criada com sucesso!");
      }
      navigate("/dashboard/filiais");
    } catch (error) {
      alert("Erro ao salvar filial");
      console.error(error);
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <Loader />;

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <PageHeader
        title={isEdit ? "Editar Filial" : "Nova Filial"}
        subtitle={isEdit ? "Atualizar dados da filial" : "Cadastrar nova filial"}
      />

      <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow max-w-4xl">
        {/* Informações Básicas */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-4">Informações Básicas</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Empresa *</label>
              <select
                name="empresa"
                value={formData.empresa}
                onChange={handleChange}
                required
                className="w-full border px-3 py-2 rounded"
              >
                <option value="">Selecione uma empresa</option>
                {empresas &&
                  empresas.map((emp) => (
                    <option key={emp.id} value={emp.id}>
                      {emp.nome}
                    </option>
                  ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Código *</label>
              <input
                type="text"
                name="codigo"
                value={formData.codigo}
                onChange={handleChange}
                required
                className="w-full border px-3 py-2 rounded"
              />
            </div>
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
              <label className="block text-sm font-medium mb-1">CNPJ</label>
              <input
                type="text"
                name="cnpj"
                value={formData.cnpj}
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
            <div>
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
                maxLength={2}
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
              <label className="block text-sm font-medium mb-1">E-mail</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
          </div>
        </div>

        {/* Configurações */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-4">Configurações</h3>
          <div className="flex flex-col gap-2">
            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                name="matriz"
                checked={formData.matriz}
                onChange={handleChange}
                className="w-4 h-4"
              />
              <label className="text-sm font-medium">É Matriz</label>
            </div>
            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                name="ativa"
                checked={formData.ativa}
                onChange={handleChange}
                className="w-4 h-4"
              />
              <label className="text-sm font-medium">Filial Ativa</label>
            </div>
          </div>
        </div>

        {/* Botões */}
        <div className="flex gap-4">
          <button
            type="submit"
            disabled={saving}
            className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {saving ? "Salvando..." : isEdit ? "Atualizar" : "Criar"}
          </button>
          <button
            type="button"
            onClick={() => navigate("/dashboard/filiais")}
            className="px-6 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
          >
            Cancelar
          </button>
        </div>
      </form>
    </div>
  );
}

