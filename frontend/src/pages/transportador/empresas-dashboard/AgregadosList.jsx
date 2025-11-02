import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Users, FileText } from 'lucide-react';
import FormModal from '../../../components/common/FormModal';
import ConfirmDialog from '../../../components/common/ConfirmDialog';
import StatusBadge from '../../../components/common/StatusBadge';
import SearchBar from '../../../components/common/SearchBar';

export default function AgregadosList() {
  const [agregados, setAgregados] = useState([]);
  const [empresas, setEmpresas] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [selectedAgregado, setSelectedAgregado] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState({
    nome: '',
    cpf: '',
    rg: '',
    cnh: '',
    categoria_cnh: '',
    vencimento_cnh: '',
    telefone: '',
    email: '',
    endereco: '',
    cidade: '',
    estado: '',
    cep: '',
    empresa_id: '',
    veiculo_placa: '',
    veiculo_modelo: '',
    data_inicio_contrato: '',
    data_fim_contrato: '',
    status: 'ativo'
  });

  useEffect(() => {
    fetchAgregados();
    fetchEmpresas();
  }, []);

  const fetchEmpresas = async () => {
    setEmpresas([
      { id: 1, nome: 'Transportadora XYZ Ltda' },
      { id: 2, nome: 'Logística ABC S/A' }
    ]);
  };

  const fetchAgregados = async () => {
    setLoading(true);
    try {
      setTimeout(() => {
        setAgregados([
          {
            id: 1,
            nome: 'Carlos Alberto Santos',
            cpf: '123.456.789-00',
            cnh: '12345678900',
            categoria_cnh: 'D',
            telefone: '(11) 99876-5432',
            email: 'carlos.santos@email.com',
            empresa: 'Transportadora XYZ Ltda',
            empresa_id: 1,
            veiculo_placa: 'ABC-1234',
            veiculo_modelo: 'Scania R450',
            data_inicio_contrato: '2024-01-15',
            status: 'ativo'
          },
          {
            id: 2,
            nome: 'José Maria Oliveira',
            cpf: '987.654.321-00',
            cnh: '98765432100',
            categoria_cnh: 'E',
            telefone: '(21) 98765-4321',
            email: 'jose.oliveira@email.com',
            empresa: 'Logística ABC S/A',
            empresa_id: 2,
            veiculo_placa: 'XYZ-5678',
            veiculo_modelo: 'Volvo FH 540',
            data_inicio_contrato: '2024-02-01',
            status: 'ativo'
          }
        ]);
        setLoading(false);
      }, 500);
    } catch (error) {
      console.error('Erro ao carregar agregados:', error);
      setLoading(false);
    }
  };

  const handleOpenModal = (agregado = null) => {
    if (agregado) {
      setSelectedAgregado(agregado);
      setFormData({
        nome: agregado.nome,
        cpf: agregado.cpf,
        rg: agregado.rg || '',
        cnh: agregado.cnh,
        categoria_cnh: agregado.categoria_cnh,
        vencimento_cnh: agregado.vencimento_cnh || '',
        telefone: agregado.telefone,
        email: agregado.email,
        endereco: agregado.endereco || '',
        cidade: agregado.cidade || '',
        estado: agregado.estado || '',
        cep: agregado.cep || '',
        empresa_id: agregado.empresa_id,
        veiculo_placa: agregado.veiculo_placa,
        veiculo_modelo: agregado.veiculo_modelo,
        data_inicio_contrato: agregado.data_inicio_contrato,
        data_fim_contrato: agregado.data_fim_contrato || '',
        status: agregado.status
      });
    } else {
      setSelectedAgregado(null);
      setFormData({
        nome: '',
        cpf: '',
        rg: '',
        cnh: '',
        categoria_cnh: '',
        vencimento_cnh: '',
        telefone: '',
        email: '',
        endereco: '',
        cidade: '',
        estado: '',
        cep: '',
        empresa_id: '',
        veiculo_placa: '',
        veiculo_modelo: '',
        data_inicio_contrato: '',
        data_fim_contrato: '',
        status: 'ativo'
      });
    }
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedAgregado(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const empresaSelecionada = empresas.find(emp => emp.id === parseInt(formData.empresa_id));
      
      if (selectedAgregado) {
        setAgregados(agregados.map(agr => 
          agr.id === selectedAgregado.id 
            ? { ...formData, id: selectedAgregado.id, empresa: empresaSelecionada?.nome } 
            : agr
        ));
      } else {
        const newAgregado = { 
          ...formData, 
          id: Date.now(), 
          empresa: empresaSelecionada?.nome 
        };
        setAgregados([...agregados, newAgregado]);
      }
      handleCloseModal();
    } catch (error) {
      console.error('Erro ao salvar agregado:', error);
    }
  };

  const handleDelete = async () => {
    try {
      setAgregados(agregados.filter(agr => agr.id !== selectedAgregado.id));
      setIsDeleteDialogOpen(false);
      setSelectedAgregado(null);
    } catch (error) {
      console.error('Erro ao excluir agregado:', error);
    }
  };

  const filteredAgregados = agregados.filter(agregado =>
    agregado.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
    agregado.cpf.includes(searchTerm) ||
    agregado.cnh.includes(searchTerm) ||
    agregado.veiculo_placa.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Agregados</h1>
          <p className="text-white/70 mt-1">Gerencie os motoristas agregados</p>
        </div>
        <button
          onClick={() => handleOpenModal()}
          className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg hover:from-purple-700 hover:to-pink-700 transition shadow-lg"
        >
          <Plus size={20} />
          Novo Agregado
        </button>
      </div>

      {/* Search Bar */}
      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
        <SearchBar 
          onSearch={setSearchTerm}
          placeholder="Buscar por nome, CPF, CNH ou placa do veículo..."
        />
      </div>

      {/* Table */}
      <div className="bg-white/5 backdrop-blur-sm rounded-lg border border-white/10 overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center p-12">
            <div className="text-center">
              <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-white/20 border-t-white"></div>
              <p className="mt-4 text-white/70">Carregando agregados...</p>
            </div>
          </div>
        ) : filteredAgregados.length === 0 ? (
          <div className="flex flex-col items-center justify-center p-12">
            <Users size={48} className="text-white/30 mb-4" />
            <p className="text-white/70 text-lg">Nenhum agregado encontrado</p>
            <p className="text-white/50 text-sm mt-2">Clique em "Novo Agregado" para cadastrar</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-white/10">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Nome</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">CPF</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">CNH</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Veículo</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Empresa</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Status</th>
                  <th className="px-6 py-4 text-right text-sm font-semibold text-white">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/10">
                {filteredAgregados.map((agregado) => (
                  <tr key={agregado.id} className="hover:bg-white/5 transition">
                    <td className="px-6 py-4">
                      <div>
                        <p className="text-white font-medium">{agregado.nome}</p>
                        <p className="text-white/60 text-sm">{agregado.telefone}</p>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-white/80">{agregado.cpf}</td>
                    <td className="px-6 py-4">
                      <div>
                        <p className="text-white">{agregado.cnh}</p>
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                          Cat. {agregado.categoria_cnh}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div>
                        <p className="text-white font-medium">{agregado.veiculo_placa}</p>
                        <p className="text-white/60 text-sm">{agregado.veiculo_modelo}</p>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-white/80">{agregado.empresa}</td>
                    <td className="px-6 py-4">
                      <StatusBadge status={agregado.status} />
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleOpenModal(agregado)}
                          className="p-2 hover:bg-blue-500/20 rounded-lg transition text-blue-400"
                          title="Editar"
                        >
                          <Edit size={18} />
                        </button>
                        <button
                          onClick={() => {
                            setSelectedAgregado(agregado);
                            setIsDeleteDialogOpen(true);
                          }}
                          className="p-2 hover:bg-red-500/20 rounded-lg transition text-red-400"
                          title="Excluir"
                        >
                          <Trash2 size={18} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Form Modal */}
      <FormModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onSubmit={handleSubmit}
        title={selectedAgregado ? 'Editar Agregado' : 'Novo Agregado'}
        size="xl"
      >
        <div className="space-y-6">
          {/* Dados Pessoais */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4 pb-2 border-b">Dados Pessoais</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Nome Completo *
                </label>
                <input
                  type="text"
                  value={formData.nome}
                  onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  CPF *
                </label>
                <input
                  type="text"
                  value={formData.cpf}
                  onChange={(e) => setFormData({ ...formData, cpf: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  RG
                </label>
                <input
                  type="text"
                  value={formData.rg}
                  onChange={(e) => setFormData({ ...formData, rg: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  CNH *
                </label>
                <input
                  type="text"
                  value={formData.cnh}
                  onChange={(e) => setFormData({ ...formData, cnh: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Categoria CNH *
                </label>
                <select
                  value={formData.categoria_cnh}
                  onChange={(e) => setFormData({ ...formData, categoria_cnh: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                  required
                >
                  <option value="">Selecione...</option>
                  <option value="C">C</option>
                  <option value="D">D</option>
                  <option value="E">E</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Vencimento CNH
                </label>
                <input
                  type="date"
                  value={formData.vencimento_cnh}
                  onChange={(e) => setFormData({ ...formData, vencimento_cnh: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Telefone *
                </label>
                <input
                  type="text"
                  value={formData.telefone}
                  onChange={(e) => setFormData({ ...formData, telefone: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  E-mail
                </label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
            </div>
          </div>

          {/* Dados do Veículo */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4 pb-2 border-b">Dados do Veículo</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Placa do Veículo *
                </label>
                <input
                  type="text"
                  value={formData.veiculo_placa}
                  onChange={(e) => setFormData({ ...formData, veiculo_placa: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Modelo do Veículo *
                </label>
                <input
                  type="text"
                  value={formData.veiculo_modelo}
                  onChange={(e) => setFormData({ ...formData, veiculo_modelo: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                  required
                />
              </div>
            </div>
          </div>

          {/* Dados do Contrato */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4 pb-2 border-b">Dados do Contrato</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Empresa *
                </label>
                <select
                  value={formData.empresa_id}
                  onChange={(e) => setFormData({ ...formData, empresa_id: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                  required
                >
                  <option value="">Selecione uma empresa...</option>
                  {empresas.map(empresa => (
                    <option key={empresa.id} value={empresa.id}>{empresa.nome}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Data Início Contrato *
                </label>
                <input
                  type="date"
                  value={formData.data_inicio_contrato}
                  onChange={(e) => setFormData({ ...formData, data_inicio_contrato: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Data Fim Contrato
                </label>
                <input
                  type="date"
                  value={formData.data_fim_contrato}
                  onChange={(e) => setFormData({ ...formData, data_fim_contrato: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Status *
                </label>
                <select
                  value={formData.status}
                  onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                  required
                >
                  <option value="ativo">Ativo</option>
                  <option value="inativo">Inativo</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </FormModal>

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={isDeleteDialogOpen}
        onClose={() => setIsDeleteDialogOpen(false)}
        onConfirm={handleDelete}
        title="Excluir Agregado"
        message={`Tem certeza que deseja excluir o agregado "${selectedAgregado?.nome}"? Esta ação não pode ser desfeita.`}
        confirmText="Excluir"
        variant="danger"
      />
    </div>
  );
}

