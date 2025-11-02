import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Package, Search, History } from 'lucide-react';
import FormModal from '../../../components/common/FormModal';
import ConfirmDialog from '../../../components/common/ConfirmDialog';
import StatusBadge from '../../../components/common/StatusBadge';
import SearchBar from '../../../components/common/SearchBar';

export default function MovimentacoesList() {
  const [movimentacoes, setMovimentacoes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [selectedMovimentacao, setSelectedMovimentacao] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState({
    item: '',
    tipo: 'entrada',
    quantidade: 0,
    data: '',
    observacoes: ''
  });

  useEffect(() => {
    fetchMovimentacoes();
  }, []);

  const fetchMovimentacoes = async () => {
    setLoading(true);
    try {
      setTimeout(() => {
        setMovimentacoes([
          {
            id: 1,
            item: 'Pneu Michelin X',
            tipo: 'entrada',
            quantidade: 10,
            data: '2025-10-14',
            observacoes: 'Recebimento de nova carga'
          },
          {
            id: 2,
            item: 'Óleo Lubrificante',
            tipo: 'saida',
            quantidade: 2,
            data: '2025-10-13',
            observacoes: 'Uso em manutenção do veículo ABC-1234'
          },
          {
            id: 3,
            item: 'Filtro de Ar',
            tipo: 'entrada',
            quantidade: 5,
            data: '2025-10-12',
            observacoes: 'Reposição de estoque'
          }
        ]);
        setLoading(false);
      }, 500);
    } catch (error) {
      console.error('Erro ao carregar movimentações:', error);
      setLoading(false);
    }
  };

  const handleOpenModal = (mov = null) => {
    if (mov) {
      setSelectedMovimentacao(mov);
      setFormData(mov);
    } else {
      setSelectedMovimentacao(null);
      setFormData({
        item: '',
        tipo: 'entrada',
        quantidade: 0,
        data: '',
        observacoes: ''
      });
    }
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedMovimentacao(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (selectedMovimentacao) {
        setMovimentacoes(movimentacoes.map(m => 
          m.id === selectedMovimentacao.id ? { ...formData, id: selectedMovimentacao.id } : m
        ));
      } else {
        const newMov = { ...formData, id: Date.now() };
        setMovimentacoes([...movimentacoes, newMov]);
      }
      handleCloseModal();
    } catch (error) {
      console.error('Erro ao salvar movimentação:', error);
    }
  };

  const handleDelete = async () => {
    try {
      setMovimentacoes(movimentacoes.filter(m => m.id !== selectedMovimentacao.id));
      setIsDeleteDialogOpen(false);
      setSelectedMovimentacao(null);
    } catch (error) {
      console.error('Erro ao excluir movimentação:', error);
    }
  };

  const filteredMovimentacoes = movimentacoes.filter(mov =>
    mov.item.toLowerCase().includes(searchTerm.toLowerCase()) ||
    mov.tipo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    mov.observacoes.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Movimentações de Estoque</h1>
          <p className="text-white/70 mt-1">Gerencie todas as entradas e saídas do seu estoque</p>
        </div>
        <button
          onClick={() => handleOpenModal()}
          className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg hover:from-green-700 hover:to-emerald-700 transition shadow-lg"
        >
          <Plus size={20} />
          Nova Movimentação
        </button>
      </div>

      {/* Search Bar */}
      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
        <SearchBar 
          onSearch={setSearchTerm}
          placeholder="Buscar por item, tipo ou observações..."
        />
      </div>

      {/* Table */}
      <div className="bg-white/5 backdrop-blur-sm rounded-lg border border-white/10 overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center p-12">
            <div className="text-center">
              <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-white/20 border-t-white"></div>
              <p className="mt-4 text-white/70">Carregando movimentações...</p>
            </div>
          </div>
        ) : filteredMovimentacoes.length === 0 ? (
          <div className="flex flex-col items-center justify-center p-12">
            <History size={48} className="text-white/30 mb-4" />
            <p className="text-white/70 text-lg">Nenhuma movimentação encontrada</p>
            <p className="text-white/50 text-sm mt-2">Clique em "Nova Movimentação" para cadastrar</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-white/10">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Item</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Tipo</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Quantidade</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Data</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Observações</th>
                  <th className="px-6 py-4 text-right text-sm font-semibold text-white">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/10">
                {filteredMovimentacoes.map((mov) => (
                  <tr key={mov.id} className="hover:bg-white/5 transition">
                    <td className="px-6 py-4 text-white font-medium">{mov.item}</td>
                    <td className="px-6 py-4">
                      <StatusBadge status={mov.tipo} type={mov.tipo === 'entrada' ? 'success' : 'danger'} />
                    </td>
                    <td className="px-6 py-4 text-white/80">{mov.quantidade}</td>
                    <td className="px-6 py-4 text-white/80">{mov.data}</td>
                    <td className="px-6 py-4 text-white/80">{mov.observacoes}</td>
                    <td className="px-6 py-4">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleOpenModal(mov)}
                          className="p-2 hover:bg-blue-500/20 rounded-lg transition text-blue-400"
                          title="Editar"
                        >
                          <Edit size={18} />
                        </button>
                        <button
                          onClick={() => {
                            setSelectedMovimentacao(mov);
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
        title={selectedMovimentacao ? 'Editar Movimentação' : 'Nova Movimentação'}
        size="md"
      >
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Item *
            </label>
            <input
              type="text"
              value={formData.item}
              onChange={(e) => setFormData({ ...formData, item: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
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
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            >
              <option value="entrada">Entrada</option>
              <option value="saida">Saída</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Quantidade *
            </label>
            <input
              type="number"
              value={formData.quantidade}
              onChange={(e) => setFormData({ ...formData, quantidade: parseInt(e.target.value) })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Data *
            </label>
            <input
              type="date"
              value={formData.data}
              onChange={(e) => setFormData({ ...formData, data: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Observações
            </label>
            <textarea
              value={formData.observacoes}
              onChange={(e) => setFormData({ ...formData, observacoes: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
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
        title="Excluir Movimentação"
        message={`Tem certeza que deseja excluir a movimentação do item "${selectedMovimentacao?.item}" (${selectedMovimentacao?.tipo})? Esta ação não pode ser desfeita.`}
        confirmText="Excluir"
        variant="danger"
      />
    </div>
  );
}

