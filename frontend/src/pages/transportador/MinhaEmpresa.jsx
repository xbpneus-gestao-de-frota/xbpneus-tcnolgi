import { useState, useEffect } from "react";
import api from "../../api/http";
import PageHeader from "../../components/PageHeader";
import Loader from "../../components/Loader";
import ErrorState from "../../components/ErrorState";

export default function MinhaEmpresa() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [editing, setEditing] = useState(false);
  const [error, setError] = useState("");
  const [saveError, setSaveError] = useState("");
  const [successMsg, setSuccessMsg] = useState("");
  
  const [form, setForm] = useState({
    nome_razao_social: "",
    cnpj: "",
    telefone: "",
    endereco: "",
    cidade: "",
    estado: "",
    cep: "",
    email: ""
  });

  useEffect(() => {
    loadEmpresa();
  }, []);

  const loadEmpresa = async () => {
    try {
      setLoading(true);
      const response = await api.get("/api/transportador/me/");
      const data = response.data;
      
      setForm({
        nome_razao_social: data.nome_razao_social || "",
        cnpj: data.cnpj || "",
        telefone: data.telefone || "",
        endereco: data.endereco || "",
        cidade: data.cidade || "",
        estado: data.estado || "",
        cep: data.cep || "",
        email: data.email || ""
      });
    } catch (ex) {
      console.error("Erro ao carregar dados da empresa:", ex);
      setError("Falha ao carregar dados da empresa.");
    } finally {
      setLoading(false);
    }
  };

  const onChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setSaveError("");
    setSuccessMsg("");

    try {
      await api.put("/api/transportador/me/", form);
      setSuccessMsg("Dados atualizados com sucesso!");
      setEditing(false);
      setTimeout(() => setSuccessMsg(""), 3000);
    } catch (ex) {
      console.error("Erro ao atualizar empresa:", ex);
      setSaveError(ex.response?.data?.detail || "Falha ao atualizar dados. Verifique os campos e tente novamente.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <Loader />;
  if (error) return <ErrorState message={error} />;

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <PageHeader 
        title="Minha Empresa" 
        subtitle="Visualize e edite os dados cadastrais da sua empresa"
      />

      <div className="bg-white rounded-xl shadow-md p-6 max-w-4xl">
        {saveError && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">
            {saveError}
          </div>
        )}
        
        {successMsg && (
          <div className="mb-4 p-4 bg-green-50 border border-green-200 text-green-700 rounded-lg">
            {successMsg}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Dados da Empresa */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-800">Dados da Empresa</h3>
              {!editing && (
                <button
                  type="button"
                  onClick={() => setEditing(true)}
                  className="px-4 py-2 rounded-lg bg-blue-500 text-white font-medium hover:bg-blue-600 transition-colors"
                >
                  Editar
                </button>
              )}
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Razão Social / Nome
                </label>
                <input
                  type="text"
                  name="nome_razao_social"
                  value={form.nome_razao_social}
                  onChange={onChange}
                  disabled={!editing}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  CNPJ
                </label>
                <input
                  type="text"
                  name="cnpj"
                  value={form.cnpj}
                  onChange={onChange}
                  disabled={!editing}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                  placeholder="00.000.000/0000-00"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  E-mail
                </label>
                <input
                  type="email"
                  name="email"
                  value={form.email}
                  onChange={onChange}
                  disabled={!editing}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Telefone
                </label>
                <input
                  type="text"
                  name="telefone"
                  value={form.telefone}
                  onChange={onChange}
                  disabled={!editing}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                  placeholder="(00) 00000-0000"
                />
              </div>
            </div>
          </div>

          {/* Endereço */}
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Endereço</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Endereço Completo
                </label>
                <input
                  type="text"
                  name="endereco"
                  value={form.endereco}
                  onChange={onChange}
                  disabled={!editing}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                  placeholder="Rua, número, complemento"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Cidade
                </label>
                <input
                  type="text"
                  name="cidade"
                  value={form.cidade}
                  onChange={onChange}
                  disabled={!editing}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Estado
                </label>
                <input
                  type="text"
                  name="estado"
                  value={form.estado}
                  onChange={onChange}
                  disabled={!editing}
                  maxLength="2"
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                  placeholder="SP"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  CEP
                </label>
                <input
                  type="text"
                  name="cep"
                  value={form.cep}
                  onChange={onChange}
                  disabled={!editing}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
                  placeholder="00000-000"
                />
              </div>
            </div>
          </div>

          {/* Botões */}
          {editing && (
            <div className="flex items-center gap-3 pt-4 border-t">
              <button
                type="submit"
                disabled={saving}
                className="px-6 py-2 rounded-lg bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 text-white font-medium hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {saving ? "Salvando..." : "Salvar Alterações"}
              </button>
              
              <button
                type="button"
                onClick={() => {
                  setEditing(false);
                  loadEmpresa();
                }}
                className="px-6 py-2 rounded-lg border border-gray-300 text-gray-700 font-medium hover:bg-gray-50 transition-colors"
              >
                Cancelar
              </button>
            </div>
          )}
        </form>
      </div>
    </div>
  );
}

