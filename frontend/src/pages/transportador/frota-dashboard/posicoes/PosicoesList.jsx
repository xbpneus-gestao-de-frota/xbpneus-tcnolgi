import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, MapPin, Layers } from 'lucide-react';
import FormModal from '../../../../components/common/FormModal';
import ConfirmDialog from '../../../../components/common/ConfirmDialog';
import StatusBadge from '../../../../components/common/StatusBadge';
import SearchBar from '../../../../components/common/SearchBar';

export default function PosicoesList() {
  const [posicoes, setPosicoes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [selectedPosicao, setSelectedPosicao] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState({
    nome: '',
    veiculo: '',
    eixo: '',
    posicao_eixo: '',
    pneu_id: null,
    status: 'livre'
  });

  useEffect(() => {
    fetchPosicoes();
  }, []);

  const fetchPosicoes = async () => {
    setLoading(true);
    try {
      setTimeout(() => {
        setPosicoes([
          {
            id: 1,
            nome: 'Eixo 1 - Posição 1',
            veiculo: 'ABC-1234',
            eixo: '1',
            posicao_eixo: '1',
            pneu_id: 101,
            status: 'ocupada'
          },
          {
            id: 2,
            nome: 'Eixo 1 - Posição 2',
            veiculo: 'ABC-1234',
            eixo: '1',
            posicao_eixo: '2',
            pneu_id: 102,
            status: 'ocupada'
          },
          {
            id: 3,
            nome: 'Eixo 2 - Posição 1',
            veiculo: 'DEF-5678',
            eixo: '2',
            posicao_eixo: '1',
            pneu_id: null,
            status: 'livre'
          },
          {
            id: 4,
            nome: 'Eixo 2 - Posição 2',
            veiculo: 'DEF-5678',
            eixo: '2',
            posicao_eixo: '2',
            pneu_id: 103,
            status: 'ocupada'
          }
        ]);
        setLoading(false);
      }, 500);
    } catch (error) {
      console.error('Erro ao carregar posições:', error);
      setLoading(false);
    }
  };

  const handleOpenModal = (posicao = null) => {
    if (posicao) {
      setSelectedPosicao(posicao);
      setFormData(posicao);
    } else {
      setSelectedPosicao(null);
      setFormData({
        nome: '',
        veiculo: '',
        eixo: '',
        posicao_eixo: '',
        pneu_id: null,
        status: 'livre'
      });
    }
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedPosicao(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (selectedPosicao) {
        setPosicoes(posicoes.map(pos => 
          pos.id === selectedPosicao.id ? { ...formData, id: selectedPosicao.id } : pos
        ));
      } else {
        const newPosicao = { ...formData, id: Date.now() };
        setPosicoes([...posicoes, newPosicao]);
      }
      handleCloseModal();
    } catch (error) {
      console.error('Erro ao salvar posição:', error);
    }
  };

  const handleDelete = async () => {
    try {
      setPosicoes(posicoes.filter(pos => pos.id !== selectedPosicao.id));
      setIsDeleteDialogOpen(false);
      setSelectedPosicao(null);
    } catch (error) {
      console.error('Erro ao excluir posição:', error);
    }
  };

  const filteredPosicoes = posicoes.filter(posicao =>
    posicao.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
    posicao.veiculo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    posicao.status.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Lista de Posições</h1>
          <p className="text-white/70 mt-1">Gerencie as posições dos pneus nos veículos</p>
        </div>
        <button
          onClick={() => handleOpenModal()}
          className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg hover:from-green-700 hover:to-emerald-700 transition shadow-lg"
        >
          <Plus size={20} />
          Nova Posição
        </button>
      </div>

      {/* Search Bar */}
      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
        <SearchBar 
          onSearch={setSearchTerm}
          placeholder="Buscar por nome, veículo ou status..."
        />
      </div>

      {/* Table */}
      <div className="bg-white/5 backdrop-blur-sm rounded-lg border border-white/10 overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center p-12">
            <div className="text-center">
              <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-white/20 border-t-white"></div>
              <p className="mt-4 text-white/70">Carregando posições...</p>
            </div>
          </div>
        ) : filteredPosicoes.length === 0 ? (
          <div className="flex flex-col items-center justify-center p-12">
            <MapPin size={48} className="text-white/30 mb-4" />
            <p className="text-white/70 text-lg">Nenhuma posição encontrada</p>
            <p className="text-white/50 text-sm mt-2">Clique em "Nova Posição" para cadastrar</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-white/10">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Nome</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Veículo</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Eixo</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Posição no Eixo</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Pneu ID</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Status</th>
                  <th className="px-6 py-4 text-right text-sm font-semibold text-white">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/10">
                {filteredPosicoes.map((posicao) => (
                  <tr key={posicao.id} className="hover:bg-white/5 transition">
                    <td className="px-6 py-4 text-white font-medium">{posicao.nome}</td>
                    <td className="px-6 py-4 text-white/80">{posicao.veiculo}</td>
                    <td className="px-6 py-4 text-white/80">{posicao.eixo}</td>
                    <td className="px-6 py-4 text-white/80">{posicao.posicao_eixo}</td>
                    <td className="px-6 py-4 text-white/80">{posicao.pneu_id || 'N/A'}</td>
                    <td className="px-6 py-4">
                      <StatusBadge status={posicao.status} />
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleOpenModal(posicao)}
                          className="p-2 hover:bg-blue-500/20 rounded-lg transition text-blue-400"
                          title="Editar"
                        >
                          <Edit size={18} />
                        </button>
                        <button
                          onClick={() => {
                            setSelectedPosicao(posicao);
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
        title={selectedPosicao ? 'Editar Posição' : 'Nova Posição'}
        size="md"
      >
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Nome da Posição *
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
              Veículo (Placa) *
            </label>
            <input
              type="text"
              value={formData.veiculo}
              onChange={(e) => setFormData({ ...formData, veiculo: e.target.value.toUpperCase() })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Eixo *
              </label>
              <input
                type="number"
                value={formData.eixo}
                onChange={(e) => setFormData({ ...formData, eixo: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Posição no Eixo *
              </label>
              <input
                type="number"
                value={formData.posicao_eixo}
                onChange={(e) => setFormData({ ...formData, posicao_eixo: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                required
              />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Pneu ID (Opcional)
            </label>
            <input
              type="number"
              value={formData.pneu_id || ''}
              onChange={(e) => setFormData({ ...formData, pneu_id: e.target.value ? parseInt(e.target.value) : null })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
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
              <option value="ocupada">Ocupada</option>
              <option value="livre">Livre</option>
              <option value="manutencao">Em Manutenção</option>
            </select>
          </div>
        </div>
      </FormModal>

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={isDeleteDialogOpen}
        onClose={() => setIsDeleteDialogOpen(false)}
        onConfirm={handleDelete}
        title="Excluir Posição"
        message={`Tem certeza que deseja excluir a posição "${selectedPosicao?.nome}"? Esta ação não pode ser desfeita.`}
        confirmText="Excluir"
        variant="danger"
      />
    </div>
  );
}

