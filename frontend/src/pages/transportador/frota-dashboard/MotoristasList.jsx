import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, UserCheck, Link as LinkIcon, AlertCircle } from 'lucide-react';
import FormModal from '../../../components/common/FormModal';
import ConfirmDialog from '../../../components/common/ConfirmDialog';
import StatusBadge from '../../../components/common/StatusBadge';
import SearchBar from '../../../components/common/SearchBar';

export default function MotoristasList() {
  const [motoristas, setMotoristas] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [isConnectionModalOpen, setIsConnectionModalOpen] = useState(false);
  const [selectedMotorista, setSelectedMotorista] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [conexaoExternaHabilitada, setConexaoExternaHabilitada] = useState(false);
  const [formData, setFormData] = useState({
    nome: '',
    cpf: '',
    rg: '',
    cnh: '',
    categoria_cnh: '',
    vencimento_cnh: '',
    data_nascimento: '',
    telefone: '',
    email: '',
    endereco: '',
    cidade: '',
    estado: '',
    cep: '',
    data_admissao: '',
    status: 'ativo'
  });

  useEffect(() => {
    fetchMotoristas();
  }, []);

  const fetchMotoristas = async () => {
    setLoading(true);
    try {
      setTimeout(() => {
        setMotoristas([
          {
            id: 1,
            nome: 'João da Silva',
            cpf: '123.456.789-00',
            cnh: '12345678900',
            categoria_cnh: 'D',
            vencimento_cnh: '2025-12-31',
            telefone: '(11) 98765-4321',
            email: 'joao.silva@email.com',
            cidade: 'São Paulo',
            estado: 'SP',
            data_admissao: '2023-01-15',
            status: 'ativo'
          },
          {
            id: 2,
            nome: 'Maria Santos',
            cpf: '987.654.321-00',
            cnh: '98765432100',
            categoria_cnh: 'E',
            vencimento_cnh: '2024-06-30',
            telefone: '(21) 91234-5678',
            email: 'maria.santos@email.com',
            cidade: 'Rio de Janeiro',
            estado: 'RJ',
            data_admissao: '2022-05-20',
            status: 'ativo'
          }
        ]);
        setLoading(false);
      }, 500);
    } catch (error) {
      console.error('Erro ao carregar motoristas:', error);
      setLoading(false);
    }
  };

  const handleOpenModal = (motorista = null) => {
    if (motorista) {
      setSelectedMotorista(motorista);
      setFormData(motorista);
    } else {
      setSelectedMotorista(null);
      setFormData({
        nome: '',
        cpf: '',
        rg: '',
        cnh: '',
        categoria_cnh: '',
        vencimento_cnh: '',
        data_nascimento: '',
        telefone: '',
        email: '',
        endereco: '',
        cidade: '',
        estado: '',
        cep: '',
        data_admissao: '',
        status: 'ativo'
      });
    }
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedMotorista(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (selectedMotorista) {
        setMotoristas(motoristas.map(mot => 
          mot.id === selectedMotorista.id ? { ...formData, id: selectedMotorista.id } : mot
        ));
      } else {
        const newMotorista = { ...formData, id: Date.now() };
        setMotoristas([...motoristas, newMotorista]);
      }
      handleCloseModal();
    } catch (error) {
      console.error('Erro ao salvar motorista:', error);
    }
  };

  const handleDelete = async () => {
    try {
      setMotoristas(motoristas.filter(mot => mot.id !== selectedMotorista.id));
      setIsDeleteDialogOpen(false);
      setSelectedMotorista(null);
    } catch (error) {
      console.error('Erro ao excluir motorista:', error);
    }
  };

  const handleToggleConexaoExterna = () => {
    setConexaoExternaHabilitada(!conexaoExternaHabilitada);
    setIsConnectionModalOpen(false);
  };

  const filteredMotoristas = motoristas.filter(motorista =>
    motorista.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
    motorista.cpf.includes(searchTerm) ||
    motorista.cnh.includes(searchTerm)
  );

  // Verificar CNH vencida ou próxima do vencimento
  const isCNHExpiring = (vencimento) => {
    const hoje = new Date();
    const dataVencimento = new Date(vencimento);
    const diasRestantes = Math.ceil((dataVencimento - hoje) / (1000 * 60 * 60 * 24));
    return diasRestantes <= 30 && diasRestantes >= 0;
  };

  const isCNHExpired = (vencimento) => {
    const hoje = new Date();
    const dataVencimento = new Date(vencimento);
    return dataVencimento < hoje;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Motoristas</h1>
          <p className="text-white/70 mt-1">Gerencie os motoristas da frota</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => setIsConnectionModalOpen(true)}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg transition shadow-lg ${
              conexaoExternaHabilitada
                ? 'bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700'
                : 'bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800'
            } text-white`}
          >
            <LinkIcon size={20} />
            {conexaoExternaHabilitada ? 'Conexão Ativa' : 'Habilitar Conexão'}
          </button>
          <button
            onClick={() => handleOpenModal()}
            className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg hover:from-green-700 hover:to-emerald-700 transition shadow-lg"
          >
            <Plus size={20} />
            Novo Motorista
          </button>
        </div>
      </div>

      {/* Connection Alert */}
      {conexaoExternaHabilitada && (
        <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4 flex items-start gap-3">
          <LinkIcon size={20} className="text-blue-400 mt-0.5" />
          <div>
            <p className="text-blue-400 font-medium">Conexão Externa Habilitada</p>
            <p className="text-blue-300/70 text-sm mt-1">
              Motoristas externos podem se conectar ao sistema através do aplicativo móvel.
            </p>
          </div>
        </div>
      )}

      {/* Search Bar */}
      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
        <SearchBar 
          onSearch={setSearchTerm}
          placeholder="Buscar por nome, CPF ou CNH..."
        />
      </div>

      {/* Table */}
      <div className="bg-white/5 backdrop-blur-sm rounded-lg border border-white/10 overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center p-12">
            <div className="text-center">
              <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-white/20 border-t-white"></div>
              <p className="mt-4 text-white/70">Carregando motoristas...</p>
            </div>
          </div>
        ) : filteredMotoristas.length === 0 ? (
          <div className="flex flex-col items-center justify-center p-12">
            <UserCheck size={48} className="text-white/30 mb-4" />
            <p className="text-white/70 text-lg">Nenhum motorista encontrado</p>
            <p className="text-white/50 text-sm mt-2">Clique em "Novo Motorista" para cadastrar</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-white/10">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Nome</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">CPF</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">CNH</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Vencimento CNH</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Cidade/UF</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Status</th>
                  <th className="px-6 py-4 text-right text-sm font-semibold text-white">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/10">
                {filteredMotoristas.map((motorista) => (
                  <tr key={motorista.id} className="hover:bg-white/5 transition">
                    <td className="px-6 py-4">
                      <div>
                        <p className="text-white font-medium">{motorista.nome}</p>
                        <p className="text-white/60 text-sm">{motorista.telefone}</p>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-white/80">{motorista.cpf}</td>
                    <td className="px-6 py-4">
                      <div>
                        <p className="text-white">{motorista.cnh}</p>
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                          Cat. {motorista.categoria_cnh}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2">
                        <span className="text-white/80">
                          {new Date(motorista.vencimento_cnh).toLocaleDateString('pt-BR')}
                        </span>
                        {isCNHExpired(motorista.vencimento_cnh) && (
                          <AlertCircle size={16} className="text-red-400" title="CNH Vencida" />
                        )}
                        {isCNHExpiring(motorista.vencimento_cnh) && !isCNHExpired(motorista.vencimento_cnh) && (
                          <AlertCircle size={16} className="text-yellow-400" title="CNH próxima do vencimento" />
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-white/80">{motorista.cidade}/{motorista.estado}</td>
                    <td className="px-6 py-4">
                      <StatusBadge status={motorista.status} />
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleOpenModal(motorista)}
                          className="p-2 hover:bg-blue-500/20 rounded-lg transition text-blue-400"
                          title="Editar"
                        >
                          <Edit size={18} />
                        </button>
                        <button
                          onClick={() => {
                            setSelectedMotorista(motorista);
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
        title={selectedMotorista ? 'Editar Motorista' : 'Novo Motorista'}
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
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
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
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
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
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Data de Nascimento *
                </label>
                <input
                  type="date"
                  value={formData.data_nascimento}
                  onChange={(e) => setFormData({ ...formData, data_nascimento: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  required
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
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
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
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              </div>
            </div>
          </div>

          {/* Dados da CNH */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4 pb-2 border-b">Dados da CNH</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Número da CNH *
                </label>
                <input
                  type="text"
                  value={formData.cnh}
                  onChange={(e) => setFormData({ ...formData, cnh: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Categoria *
                </label>
                <select
                  value={formData.categoria_cnh}
                  onChange={(e) => setFormData({ ...formData, categoria_cnh: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
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
                  Vencimento *
                </label>
                <input
                  type="date"
                  value={formData.vencimento_cnh}
                  onChange={(e) => setFormData({ ...formData, vencimento_cnh: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  required
                />
              </div>
            </div>
          </div>

          {/* Endereço */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4 pb-2 border-b">Endereço</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Endereço
                </label>
                <input
                  type="text"
                  value={formData.endereco}
                  onChange={(e) => setFormData({ ...formData, endereco: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Cidade *
                </label>
                <input
                  type="text"
                  value={formData.cidade}
                  onChange={(e) => setFormData({ ...formData, cidade: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Estado *
                </label>
                <select
                  value={formData.estado}
                  onChange={(e) => setFormData({ ...formData, estado: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  required
                >
                  <option value="">Selecione...</option>
                  <option value="SP">São Paulo</option>
                  <option value="RJ">Rio de Janeiro</option>
                  <option value="MG">Minas Gerais</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  CEP
                </label>
                <input
                  type="text"
                  value={formData.cep}
                  onChange={(e) => setFormData({ ...formData, cep: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Data de Admissão *
                </label>
                <input
                  type="date"
                  value={formData.data_admissao}
                  onChange={(e) => setFormData({ ...formData, data_admissao: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Status *
                </label>
                <select
                  value={formData.status}
                  onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  required
                >
                  <option value="ativo">Ativo</option>
                  <option value="inativo">Inativo</option>
                  <option value="ferias">Férias</option>
                  <option value="afastado">Afastado</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </FormModal>

      {/* Connection Modal */}
      <FormModal
        isOpen={isConnectionModalOpen}
        onClose={() => setIsConnectionModalOpen(false)}
        onSubmit={(e) => {
          e.preventDefault();
          handleToggleConexaoExterna();
        }}
        title="Conexão Externa de Motoristas"
        size="md"
      >
        <div className="space-y-4">
          <div className="flex items-start gap-3 p-4 bg-blue-50 rounded-lg">
            <LinkIcon size={20} className="text-blue-600 mt-0.5" />
            <div>
              <p className="text-gray-900 font-medium">O que é Conexão Externa?</p>
              <p className="text-gray-600 text-sm mt-1">
                Permite que motoristas se conectem ao sistema através do aplicativo móvel, 
                acessando informações de viagens, entregas e documentos.
              </p>
            </div>
          </div>

          <div className="space-y-2">
            <p className="text-gray-700 font-medium">Status Atual:</p>
            <p className={`text-sm ${conexaoExternaHabilitada ? 'text-green-600' : 'text-gray-500'}`}>
              {conexaoExternaHabilitada ? '✓ Conexão habilitada' : '✗ Conexão desabilitada'}
            </p>
          </div>

          <div className="pt-4 border-t">
            <button
              type="submit"
              className={`w-full px-4 py-2 rounded-lg font-medium transition ${
                conexaoExternaHabilitada
                  ? 'bg-red-600 hover:bg-red-700 text-white'
                  : 'bg-green-600 hover:bg-green-700 text-white'
              }`}
            >
              {conexaoExternaHabilitada ? 'Desabilitar Conexão' : 'Habilitar Conexão'}
            </button>
          </div>
        </div>
      </FormModal>

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={isDeleteDialogOpen}
        onClose={() => setIsDeleteDialogOpen(false)}
        onConfirm={handleDelete}
        title="Excluir Motorista"
        message={`Tem certeza que deseja excluir o motorista "${selectedMotorista?.nome}"? Esta ação não pode ser desfeita.`}
        confirmText="Excluir"
        variant="danger"
      />
    </div>
  );
}

