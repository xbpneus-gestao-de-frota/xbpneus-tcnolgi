import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Wrench, Search, FileText } from 'lucide-react';
import FormModal from '../../../components/common/FormModal';
import ConfirmDialog from '../../../components/common/ConfirmDialog';
import StatusBadge from '../../../components/common/StatusBadge';
import SearchBar from '../../../components/common/SearchBar';

export default function OSList() {
  const [ordensServico, setOrdensServico] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [selectedOS, setSelectedOS] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState({
    veiculo: '',
    tipo: 'preventiva',
    status: 'aberta',
    dataAbertura: '',
    dataConclusao: '',
    descricao: ''
  });

  useEffect(() => {
    fetchOrdensServico();
  }, []);

  const fetchOrdensServico = async () => {
    setLoading(true);
    try {
      setTimeout(() => {
        setOrdensServico([
          {
            id: 1,
            veiculo: 'ABC-1234',
            tipo: 'preventiva',
            status: 'aberta',
            dataAbertura: '2025-10-10',
            dataConclusao: '',
            descricao: 'Troca de óleo e filtros'
          },
          {
            id: 2,
            veiculo: 'DEF-5678',
            tipo: 'corretiva',
            status: 'concluida',
            dataAbertura: '2025-10-05',
            dataConclusao: '2025-10-08',
            descricao: 'Reparo no sistema de freios'
          },
          {
            id: 3,
            veiculo: 'GHI-9012',
            tipo: 'preditiva',
            status: 'em_andamento',
            dataAbertura: '2025-10-12',
            dataConclusao: '',
            descricao: 'Análise de vibração no motor'
          }
        ]);
        setLoading(false);
      }, 500);
    } catch (error) {
      console.error('Erro ao carregar ordens de serviço:', error);
      setLoading(false);
    }
  };

  const handleOpenModal = (os = null) => {
    if (os) {
      setSelectedOS(os);
      setFormData(os);
    } else {
      setSelectedOS(null);
      setFormData({
        veiculo: '',
        tipo: 'preventiva',
        status: 'aberta',
        dataAbertura: '',
        dataConclusao: '',
        descricao: ''
      });
    }
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedOS(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (selectedOS) {
        setOrdensServico(ordensServico.map(os => 
          os.id === selectedOS.id ? { ...formData, id: selectedOS.id } : os
        ));
      } else {
        const newOS = { ...formData, id: Date.now() };
        setOrdensServico([...ordensServico, newOS]);
      }
      handleCloseModal();
    } catch (error) {
      console.error('Erro ao salvar ordem de serviço:', error);
    }
  };

  const handleDelete = async () => {
    try {
      setOrdensServico(ordensServico.filter(os => os.id !== selectedOS.id));
      setIsDeleteDialogOpen(false);
      setSelectedOS(null);
    } catch (error) {
      console.error('Erro ao excluir ordem de serviço:', error);
    }
  };

  const filteredOS = ordensServico.filter(os =>
    os.veiculo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    os.tipo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    os.status.toLowerCase().includes(searchTerm.toLowerCase()) ||
    os.descricao.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusColor = (status) => {
    switch (status) {
      case 'aberta': return 'blue';
      case 'em_andamento': return 'orange';
      case 'concluida': return 'green';
      case 'cancelada': return 'red';
      default: return 'gray';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Ordens de Serviço</h1>
          <p className="text-white/70 mt-1">Gerencie todas as ordens de serviço da sua frota</p>
        </div>
        <button
          onClick={() => handleOpenModal()}
          className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg hover:from-green-700 hover:to-emerald-700 transition shadow-lg"
        >
          <Plus size={20} />
          Nova OS
        </button>
      </div>

      {/* Search Bar */}
      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
        <SearchBar 
          onSearch={setSearchTerm}
          placeholder="Buscar por veículo, tipo, status ou descrição..."
        />
      </div>

      {/* Table */}
      <div className="bg-white/5 backdrop-blur-sm rounded-lg border border-white/10 overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center p-12">
            <div className="text-center">
              <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-white/20 border-t-white"></div>
              <p className="mt-4 text-white/70">Carregando ordens de serviço...</p>
            </div>
          </div>
        ) : filteredOS.length === 0 ? (
          <div className="flex flex-col items-center justify-center p-12">
            <Wrench size={48} className="text-white/30 mb-4" />
            <p className="text-white/70 text-lg">Nenhuma ordem de serviço encontrada</p>
            <p className="text-white/50 text-sm mt-2">Clique em "Nova OS" para cadastrar</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-white/10">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Veículo</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Tipo</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Status</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Abertura</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Conclusão</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Descrição</th>
                  <th className="px-6 py-4 text-right text-sm font-semibold text-white">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/10">
                {filteredOS.map((os) => (
                  <tr key={os.id} className="hover:bg-white/5 transition">
                    <td className="px-6 py-4 text-white font-medium">{os.veiculo}</td>
                    <td className="px-6 py-4 text-white/80">{os.tipo.charAt(0).toUpperCase() + os.tipo.slice(1)}</td>
                    <td className="px-6 py-4">
                      <StatusBadge status={os.status} type={getStatusColor(os.status)} />
                    </td>
                    <td className="px-6 py-4 text-white/80">{os.dataAbertura}</td>
                    <td className="px-6 py-4 text-white/80">{os.dataConclusao || 'N/A'}</td>
                    <td className="px-6 py-4 text-white/80">{os.descricao}</td>
                    <td className="px-6 py-4">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleOpenModal(os)}
                          className="p-2 hover:bg-blue-500/20 rounded-lg transition text-blue-400"
                          title="Editar"
                        >
                          <Edit size={18} />
                        </button>
                        <button
                          onClick={() => {
                            setSelectedOS(os);
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
        title={selectedOS ? 'Editar Ordem de Serviço' : 'Nova Ordem de Serviço'}
        size="lg"
      >
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Veículo *
            </label>
            <input
              type="text"
              value={formData.veiculo}
              onChange={(e) => setFormData({ ...formData, veiculo: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tipo *
            </label>
            <select
              value={formData.tipo}
              onChange={(e) => setFormData({ ...formData, tipo: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="preventiva">Preventiva</option>
              <option value="corretiva">Corretiva</option>
              <option value="preditiva">Preditiva</option>
            </select>
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
              <option value="aberta">Aberta</option>
              <option value="em_andamento">Em Andamento</option>
              <option value="concluida">Concluída</option>
              <option value="cancelada">Cancelada</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Data de Abertura *
            </label>
            <input
              type="date"
              value={formData.dataAbertura}
              onChange={(e) => setFormData({ ...formData, dataAbertura: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Data de Conclusão
            </label>
            <input
              type="date"
              value={formData.dataConclusao}
              onChange={(e) => setFormData({ ...formData, dataConclusao: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Descrição
            </label>
            <textarea
              value={formData.descricao}
              onChange={(e) => setFormData({ ...formData, descricao: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows="3"
            ></textarea>
          </div>
        </div>
      </FormModal>

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={isDeleteDialogOpen}
        onClose={() => setIsDeleteDialogOpen(false)}
        onConfirm={handleDelete}
        title="Excluir Ordem de Serviço"
        message={`Tem certeza que deseja excluir a OS do veículo "${selectedOS?.veiculo}" (${selectedOS?.tipo})? Esta ação não pode ser desfeita.`}
        confirmText="Excluir"
        variant="danger"
      />
    </div>
  );
}

