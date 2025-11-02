import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../../api/http";
import PageHeader from "../../../components/PageHeader";
import Button from "../../../components/ui/Button";

export default function VeiculoCreate() {
  const navigate = useNavigate();
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [empresas, setEmpresas] = useState([]);
  const [filiais, setFiliais] = useState([]);
  const [modelosVeiculos, setModelosVeiculos] = useState([]);
  const [operacoesConfiguracoes, setOperacoesConfiguracoes] = useState([]);
  
  const [form, setForm] = useState({
    empresa: "",
    filial: "",
    placa: "",
    modelo_veiculo: "",
    configuracao_operacional: "",
    ano_fabricacao: "",
    ano_modelo: "",
    tipo: "CAMINHAO",
    status: "ATIVO",
    km: "0",
    km_ultima_manutencao: "0",
    km_proxima_manutencao: "",
    motorista: "",
    chassi: "",
    renavam: "",
    capacidade_carga: "",
    data_aquisicao: "",
    observacoes: ""
  });

  // Carregar dados dos catálogos
  const loadCatalogos = useCallback(async () => {
    try {
      const [empresasRes, modelosRes, operacoesRes] = await Promise.all([
        api.get("/api/transportador/empresas/empresas/"),
        api.get("/api/transportador/configuracoes/catalogo-modelos-veiculos/"),
        api.get("/api/transportador/configuracoes/operacoes-configuracoes/")
      ]);
      setEmpresas(empresasRes.data.results || empresasRes.data || []);
      setModelosVeiculos(modelosRes.data.results || modelosRes.data || []);
      setOperacoesConfiguracoes(operacoesRes.data.results || operacoesRes.data || []);
    } catch (error) {
      console.error("Erro ao carregar catálogos:", error);
    }
  }, []);

  useEffect(() => {
    loadCatalogos();
  }, [loadCatalogos]);

  // Carregar filiais quando empresa for selecionada
  useEffect(() => {
    if (form.empresa) {
      loadFiliais(form.empresa);
    } else {
      setFiliais([]);
      setForm(prev => ({ ...prev, filial: "" }));
    }
  }, [form.empresa]);

  const loadFiliais = async (empresaId) => {
    try {
      const response = await api.get(`/api/transportador/empresas/filiais/?empresa=${empresaId}`);
      setFiliais(response.data.results || response.data || []);
    } catch (error) {
      console.error("Erro ao carregar filiais:", error);
    }
  };

  const onChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError("");

    try {
      const payload = {
        empresa: form.empresa ? parseInt(form.empresa) : null,
        filial: form.filial ? parseInt(form.filial) : null,
        placa: form.placa,
        modelo_veiculo: form.modelo_veiculo ? parseInt(form.modelo_veiculo) : null,
        configuracao_operacional: form.configuracao_operacional ? parseInt(form.configuracao_operacional) : null,
        ano_fabricacao: form.ano_fabricacao ? parseInt(form.ano_fabricacao) : null,
        ano_modelo: form.ano_modelo ? parseInt(form.ano_modelo) : null,
        tipo: form.tipo,
        status: form.status,
        km: parseInt(form.km) || 0,
        km_ultima_manutencao: parseInt(form.km_ultima_manutencao) || 0,
        km_proxima_manutencao: form.km_proxima_manutencao ? parseInt(form.km_proxima_manutencao) : null,
        motorista: form.motorista || null,
        chassi: form.chassi || null,
        renavam: form.renavam || null,
        capacidade_carga: form.capacidade_carga ? parseFloat(form.capacidade_carga) : null,
        data_aquisicao: form.data_aquisicao || null,
        observacoes: form.observacoes || null
      };

      await api.post("/api/transportador/frota/veiculos/", payload);
      navigate("/dashboard/frota/veiculos");
    } catch (ex) {
      console.error("Erro ao criar veículo:", ex);
      setError(ex.response?.data?.detail || "Falha ao criar veículo. Verifique os dados e tente novamente.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <PageHeader 
        title="Novo Veículo" 
        subtitle="Cadastrar novo veículo na frota"
      />

      <div className="bg-white rounded-xl shadow-md p-6 max-w-4xl">
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Empresa e Filial */}
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Empresa e Filial</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Empresa</label>
                <select
                  name="empresa"
                  value={form.empresa}
                  onChange={onChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Selecione uma empresa</option>
                  {empresas.map((emp) => (
                    <option key={emp.id} value={emp.id}>
                      {emp.nome}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Filial</label>
                <select
                  name="filial"
                  value={form.filial}
                  onChange={onChange}
                  disabled={!form.empresa}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
                >
                  <option value="">Selecione uma filial</option>
                  {filiais.map((fil) => (
                    <option key={fil.id} value={fil.id}>
                      {fil.codigo} - {fil.nome}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Dados Básicos */}
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Dados Básicos</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Placa <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  name="placa"
                  value={form.placa}
                  onChange={onChange}
                  required
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="ABC1D23"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Modelo do Veículo</label>
                <select
                  name="modelo_veiculo"
                  value={form.modelo_veiculo}
                  onChange={onChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Selecione um modelo</option>
                  {modelosVeiculos.map((modelo) => (
                    <option key={modelo.id} value={modelo.id}>
                      {modelo.marca} {modelo.familia_modelo} {modelo.variante}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Configuração Operacional</label>
                <select
                  name="configuracao_operacional"
                  value={form.configuracao_operacional}
                  onChange={onChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Selecione uma configuração</option>
                  {operacoesConfiguracoes.map((op) => (
                    <option key={op.id} value={op.id}>
                      {op.op_code}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Tipo</label>
                <select
                  name="tipo"
                  value={form.tipo}
                  onChange={onChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="CAMINHAO">Caminhão</option>
                  <option value="CARRETA">Carreta</option>
                  <option value="BITREM">Bitrem</option>
                  <option value="RODOTREM">Rodotrem</option>
                  <option value="VUC">VUC</option>
                  <option value="OUTRO">Outro</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                <select
                  name="status"
                  value={form.status}
                  onChange={onChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="ATIVO">Ativo</option>
                  <option value="MANUTENCAO">Em Manutenção</option>
                  <option value="INATIVO">Inativo</option>
                  <option value="VENDIDO">Vendido</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Ano Fabricação</label>
                <input
                  type="number"
                  name="ano_fabricacao"
                  value={form.ano_fabricacao}
                  onChange={onChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="2020"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Ano Modelo</label>
                <input
                  type="number"
                  name="ano_modelo"
                  value={form.ano_modelo}
                  onChange={onChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="2021"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Data de Aquisição</label>
                <input
                  type="date"
                  name="data_aquisicao"
                  value={form.data_aquisicao}
                  onChange={onChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
          </div>

          {/* Dados Técnicos */}
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Dados Técnicos</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Chassi</label>
                <input
                  type="text"
                  name="chassi"
                  value={form.chassi}
                  onChange={onChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="9BW..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Renavam</label>
                <input
                  type="text"
                  name="renavam"
                  value={form.renavam}
                  onChange={onChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="00000000000"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Capacidade de Carga (ton)
                </label>
                <input
                  type="number"
                  step="0.01"
                  name="capacidade_carga"
                  value={form.capacidade_carga}
                  onChange={onChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="25.00"
                />
              </div>
            </div>
          </div>

          {/* Dados Operacionais */}
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Dados Operacionais</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Quilometragem Atual
                </label>
                <input
                  type="number"
                  name="km"
                  value={form.km}
                  onChange={onChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="0"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  KM Última Manutenção
                </label>
                <input
                  type="number"
                  name="km_ultima_manutencao"
                  value={form.km_ultima_manutencao}
                  onChange={onChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="0"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  KM Próxima Manutenção
                </label>
                <input
                  type="number"
                  name="km_proxima_manutencao"
                  value={form.km_proxima_manutencao}
                  onChange={onChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="10000"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Motorista Atual
                </label>
                <input
                  type="text"
                  name="motorista"
                  value={form.motorista}
                  onChange={onChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Nome do motorista"
                />
              </div>
            </div>
          </div>

          {/* Observações */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Observações</label>
            <textarea
              name="observacoes"
              value={form.observacoes}
              onChange={onChange}
              rows="3"
              className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Detalhes adicionais sobre o veículo"
            ></textarea>
          </div>

          <div className="flex justify-end space-x-4">
            <Button 
              type="button" 
              variant="secondary"
              onClick={() => navigate("/dashboard/frota/veiculos")}
              disabled={saving}
            >
              Cancelar
            </Button>
            <Button 
              type="submit" 
              variant="primary"
              disabled={saving}
            >
              {saving ? "Salvando..." : "Salvar Veículo"}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}

