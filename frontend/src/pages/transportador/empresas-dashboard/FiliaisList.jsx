import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, MapPin } from 'lucide-react';
import FormModal from '../../../components/common/FormModal';
import ConfirmDialog from '../../../components/common/ConfirmDialog';
import StatusBadge from '../../../components/common/StatusBadge';
import SearchBar from '../../../components/common/SearchBar';

export default function FiliaisList() {
  const [filiais, setFiliais] = useState([]);
  const [empresas, setEmpresas] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [selectedFilial, setSelectedFilial] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState({
    nome: '',
    empresa_id: '',
    codigo: '',
    telefone: '',
    email: '',
    endereco: '',
    cidade: '',
    estado: '',
    cep: '',
    responsavel: '',
    status: 'ativo'
  });

  useEffect(() => {
    fetchFiliais();
    fetchEmpresas();
  }, []);

  const fetchEmpresas = async () => {
    // Simulando dados de empresas
    setEmpresas([
      { id: 1, nome: 'Transportadora XYZ Ltda' },
      { id: 2, nome: 'Logística ABC S/A' }
    ]);
  };

  const fetchFiliais = async () => {
    setLoading(true);
    try {
      setTimeout(() => {
        setFiliais([
          {
            id: 1,
            nome: 'Filial São Paulo - Centro',
            empresa: 'Transportadora XYZ Ltda',
            empresa_id: 1,
            codigo: 'SP-001',
            telefone: '(11) 3456-7890',
            email: 'sp.centro@xyz.com.br',
            cidade: 'São Paulo',
            estado: 'SP',
            responsavel: 'João Silva',
            status: 'ativo'
          },
          {
            id: 2,
            nome: 'Filial Rio de Janeiro',
            empresa: 'Logística ABC S/A',
            empresa_id: 2,
            codigo: 'RJ-001',
            telefone: '(21) 2345-6789',
            email: 'rj@abc.com.br',
            cidade: 'Rio de Janeiro',
            estado: 'RJ',
            responsavel: 'Maria Santos',
            status: 'ativo'
          }
        ]);
        setLoading(false);
      }, 500);
    } catch (error) {
      console.error('Erro ao carregar filiais:', error);
      setLoading(false);
    }
  };

  const handleOpenModal = (filial = null) => {
    if (filial) {
      setSelectedFilial(filial);
      setFormData({
        nome: filial.nome,
        empresa_id: filial.empresa_id,
        codigo: filial.codigo,
        telefone: filial.telefone,
        email: filial.email,
        endereco: filial.endereco || '',
        cidade: filial.cidade,
        estado: filial.estado,
        cep: filial.cep || '',
        responsavel: filial.responsavel,
        status: filial.status
      });
    } else {
      setSelectedFilial(null);
      setFormData({
        nome: '',
        empresa_id: '',
        codigo: '',
        telefone: '',
        email: '',
        endereco: '',
        cidade: '',
        estado: '',
        cep: '',
        responsavel: '',
        status: 'ativo'
      });
    }
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedFilial(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const empresaSelecionada = empresas.find(emp => emp.id === parseInt(formData.empresa_id));
      
      if (selectedFilial) {
        setFiliais(filiais.map(fil => 
          fil.id === selectedFilial.id 
            ? { ...formData, id: selectedFilial.id, empresa: empresaSelecionada?.nome } 
            : fil
        ));
      } else {
        const newFilial = { 
          ...formData, 
          id: Date.now(), 
          empresa: empresaSelecionada?.nome 
        };
        setFiliais([...filiais, newFilial]);
      }
      handleCloseModal();
    } catch (error) {
      console.error('Erro ao salvar filial:', error);
    }
  };

  const handleDelete = async () => {
    try {
      setFiliais(filiais.filter(fil => fil.id !== selectedFilial.id));
      setIsDeleteDialogOpen(false);
      setSelectedFilial(null);
    } catch (error) {
      console.error('Erro ao excluir filial:', error);
    }
  };

  const filteredFiliais = filiais.filter(filial =>
    filial.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
    filial.codigo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    filial.cidade.toLowerCase().includes(searchTerm.toLowerCase()) ||
    filial.empresa.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Filiais</h1>
          <p className="text-white/70 mt-1">Gerencie as filiais e unidades operacionais</p>
        </div>
        <button
          onClick={() => handleOpenModal()}
          className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg hover:from-green-700 hover:to-emerald-700 transition shadow-lg"
        >
          <Plus size={20} />
          Nova Filial
        </button>
      </div>

      {/* Search Bar */}
      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
        <SearchBar 
          onSearch={setSearchTerm}
          placeholder="Buscar por nome, código, cidade ou empresa..."
        />
      </div>

      {/* Table */}
      <div className="bg-white/5 backdrop-blur-sm rounded-lg border border-white/10 overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center p-12">
            <div className="text-center">
              <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-white/20 border-t-white"></div>
              <p className="mt-4 text-white/70">Carregando filiais...</p>
            </div>
          </div>
        ) : filteredFiliais.length === 0 ? (
          <div className="flex flex-col items-center justify-center p-12">
            <MapPin size={48} className="text-white/30 mb-4" />
            <p className="text-white/70 text-lg">Nenhuma filial encontrada</p>
            <p className="text-white/50 text-sm mt-2">Clique em "Nova Filial" para cadastrar</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-white/10">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Código</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Nome</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Empresa</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Cidade/UF</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Responsável</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Status</th>
                  <th className="px-6 py-4 text-right text-sm font-semibold text-white">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/10">
                {filteredFiliais.map((filial) => (
                  <tr key={filial.id} className="hover:bg-white/5 transition">
                    <td className="px-6 py-4">
                      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-500/20 text-blue-300 border border-blue-500/30">
                        {filial.codigo}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div>
                        <p className="text-white font-medium">{filial.nome}</p>
                        <p className="text-white/60 text-sm">{filial.telefone}</p>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-white/80">{filial.empresa}</td>
                    <td className="px-6 py-4 text-white/80">{filial.cidade}/{filial.estado}</td>
                    <td className="px-6 py-4 text-white/80">{filial.responsavel}</td>
                    <td className="px-6 py-4">
                      <StatusBadge status={filial.status} />
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleOpenModal(filial)}
                          className="p-2 hover:bg-blue-500/20 rounded-lg transition text-blue-400"
                          title="Editar"
                        >
                          <Edit size={18} />
                        </button>
                        <button
                          onClick={() => {
                            setSelectedFilial(filial);
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
        title={selectedFilial ? 'Editar Filial' : 'Nova Filial'}
        size="lg"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Empresa *
            </label>
            <select
              value={formData.empresa_id}
              onChange={(e) => setFormData({ ...formData, empresa_id: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
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
              Código *
            </label>
            <input
              type="text"
              value={formData.codigo}
              onChange={(e) => setFormData({ ...formData, codigo: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="Ex: SP-001"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Nome da Filial *
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
              E-mail *
            </label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
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
              Responsável *
            </label>
            <input
              type="text"
              value={formData.responsavel}
              onChange={(e) => setFormData({ ...formData, responsavel: e.target.value })}
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
            </select>
          </div>
        </div>
      </FormModal>

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={isDeleteDialogOpen}
        onClose={() => setIsDeleteDialogOpen(false)}
        onConfirm={handleDelete}
        title="Excluir Filial"
        message={`Tem certeza que deseja excluir a filial "${selectedFilial?.nome}"? Esta ação não pode ser desfeita.`}
        confirmText="Excluir"
        variant="danger"
      />
    </div>
  );
}

