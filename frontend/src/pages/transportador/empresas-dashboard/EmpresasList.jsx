import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Search, Building2 } from 'lucide-react';
import FormModal from '../../../components/common/FormModal';
import ConfirmDialog from '../../../components/common/ConfirmDialog';
import StatusBadge from '../../../components/common/StatusBadge';
import SearchBar from '../../../components/common/SearchBar';

export default function EmpresasList() {
  const [empresas, setEmpresas] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [selectedEmpresa, setSelectedEmpresa] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState({
    nome: '',
    razao_social: '',
    cnpj: '',
    inscricao_estadual: '',
    telefone: '',
    email: '',
    endereco: '',
    cidade: '',
    estado: '',
    cep: '',
    status: 'ativo'
  });

  useEffect(() => {
    fetchEmpresas();
  }, []);

  const fetchEmpresas = async () => {
    setLoading(true);
    try {
      // Simulando dados - em produção, fazer chamada à API
      setTimeout(() => {
        setEmpresas([
          {
            id: 1,
            nome: 'Transportadora XYZ Ltda',
            razao_social: 'XYZ Transportes e Logística Ltda',
            cnpj: '12.345.678/0001-90',
            telefone: '(11) 98765-4321',
            email: 'contato@xyz.com.br',
            cidade: 'São Paulo',
            estado: 'SP',
            status: 'ativo'
          },
          {
            id: 2,
            nome: 'Logística ABC S/A',
            razao_social: 'ABC Logística e Transportes S/A',
            cnpj: '98.765.432/0001-10',
            telefone: '(21) 91234-5678',
            email: 'contato@abc.com.br',
            cidade: 'Rio de Janeiro',
            estado: 'RJ',
            status: 'ativo'
          }
        ]);
        setLoading(false);
      }, 500);
    } catch (error) {
      console.error('Erro ao carregar empresas:', error);
      setLoading(false);
    }
  };

  const handleOpenModal = (empresa = null) => {
    if (empresa) {
      setSelectedEmpresa(empresa);
      setFormData(empresa);
    } else {
      setSelectedEmpresa(null);
      setFormData({
        nome: '',
        razao_social: '',
        cnpj: '',
        inscricao_estadual: '',
        telefone: '',
        email: '',
        endereco: '',
        cidade: '',
        estado: '',
        cep: '',
        status: 'ativo'
      });
    }
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedEmpresa(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Simulando salvamento - em produção, fazer chamada à API
      if (selectedEmpresa) {
        // Atualizar empresa existente
        setEmpresas(empresas.map(emp => 
          emp.id === selectedEmpresa.id ? { ...formData, id: selectedEmpresa.id } : emp
        ));
      } else {
        // Criar nova empresa
        const newEmpresa = { ...formData, id: Date.now() };
        setEmpresas([...empresas, newEmpresa]);
      }
      handleCloseModal();
    } catch (error) {
      console.error('Erro ao salvar empresa:', error);
    }
  };

  const handleDelete = async () => {
    try {
      // Simulando exclusão - em produção, fazer chamada à API
      setEmpresas(empresas.filter(emp => emp.id !== selectedEmpresa.id));
      setIsDeleteDialogOpen(false);
      setSelectedEmpresa(null);
    } catch (error) {
      console.error('Erro ao excluir empresa:', error);
    }
  };

  const filteredEmpresas = empresas.filter(empresa =>
    empresa.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
    empresa.cnpj.includes(searchTerm) ||
    empresa.cidade.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Empresas</h1>
          <p className="text-white/70 mt-1">Gerencie as empresas do grupo</p>
        </div>
        <button
          onClick={() => handleOpenModal()}
          className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition shadow-lg"
        >
          <Plus size={20} />
          Nova Empresa
        </button>
      </div>

      {/* Search Bar */}
      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
        <SearchBar 
          onSearch={setSearchTerm}
          placeholder="Buscar por nome, CNPJ ou cidade..."
        />
      </div>

      {/* Table */}
      <div className="bg-white/5 backdrop-blur-sm rounded-lg border border-white/10 overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center p-12">
            <div className="text-center">
              <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-white/20 border-t-white"></div>
              <p className="mt-4 text-white/70">Carregando empresas...</p>
            </div>
          </div>
        ) : filteredEmpresas.length === 0 ? (
          <div className="flex flex-col items-center justify-center p-12">
            <Building2 size={48} className="text-white/30 mb-4" />
            <p className="text-white/70 text-lg">Nenhuma empresa encontrada</p>
            <p className="text-white/50 text-sm mt-2">Clique em "Nova Empresa" para cadastrar</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-white/10">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Nome</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">CNPJ</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Telefone</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Cidade/UF</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Status</th>
                  <th className="px-6 py-4 text-right text-sm font-semibold text-white">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/10">
                {filteredEmpresas.map((empresa) => (
                  <tr key={empresa.id} className="hover:bg-white/5 transition">
                    <td className="px-6 py-4">
                      <div>
                        <p className="text-white font-medium">{empresa.nome}</p>
                        <p className="text-white/60 text-sm">{empresa.razao_social}</p>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-white/80">{empresa.cnpj}</td>
                    <td className="px-6 py-4 text-white/80">{empresa.telefone}</td>
                    <td className="px-6 py-4 text-white/80">{empresa.cidade}/{empresa.estado}</td>
                    <td className="px-6 py-4">
                      <StatusBadge status={empresa.status} />
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleOpenModal(empresa)}
                          className="p-2 hover:bg-blue-500/20 rounded-lg transition text-blue-400"
                          title="Editar"
                        >
                          <Edit size={18} />
                        </button>
                        <button
                          onClick={() => {
                            setSelectedEmpresa(empresa);
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
        title={selectedEmpresa ? 'Editar Empresa' : 'Nova Empresa'}
        size="lg"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Nome Fantasia *
            </label>
            <input
              type="text"
              value={formData.nome}
              onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Razão Social *
            </label>
            <input
              type="text"
              value={formData.razao_social}
              onChange={(e) => setFormData({ ...formData, razao_social: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              CNPJ *
            </label>
            <input
              type="text"
              value={formData.cnpj}
              onChange={(e) => setFormData({ ...formData, cnpj: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Inscrição Estadual
            </label>
            <input
              type="text"
              value={formData.inscricao_estadual}
              onChange={(e) => setFormData({ ...formData, inscricao_estadual: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
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
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              E-mail *
            </label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Endereço
            </label>
            <input
              type="text"
              value={formData.endereco}
              onChange={(e) => setFormData({ ...formData, endereco: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
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
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
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
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="">Selecione...</option>
              <option value="SP">São Paulo</option>
              <option value="RJ">Rio de Janeiro</option>
              <option value="MG">Minas Gerais</option>
              {/* Adicionar outros estados */}
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
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Status *
            </label>
            <select
              value={formData.status}
              onChange={(e) => setFormData({ ...formData, status: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="ativo">Ativo</option>
              <option value="inativo">Inativo</option>
            </select>
          </div>
        </div>
      </FormModal>

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={isDeleteDialogOpen}
        onClose={() => setIsDeleteDialogOpen(false)}
        onConfirm={handleDelete}
        title="Excluir Empresa"
        message={`Tem certeza que deseja excluir a empresa "${selectedEmpresa?.nome}"? Esta ação não pode ser desfeita.`}
        confirmText="Excluir"
        variant="danger"
      />
    </div>
  );
}

