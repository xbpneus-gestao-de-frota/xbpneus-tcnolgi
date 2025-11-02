import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Gauge, Search } from 'lucide-react';
import FormModal from '../../../components/common/FormModal';
import ConfirmDialog from '../../../components/common/ConfirmDialog';
import StatusBadge from '../../../components/common/StatusBadge';
import SearchBar from '../../../components/common/SearchBar';

export default function PneusList() {
  const [pneus, setPneus] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [selectedPneu, setSelectedPneu] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState({
    marca: '',
    modelo: '',
    numero_serie: '',
    tipo: 'radial',
    status: 'estoque',
    vida_util_km: 0,
    data_fabricacao: ''
  });

  useEffect(() => {
    fetchPneus();
  }, []);

  const fetchPneus = async () => {
    setLoading(true);
    try {
      setTimeout(() => {
        setPneus([
          {
            id: 1,
            marca: 'Michelin',
            modelo: 'X MultiWay 3D',
            numero_serie: 'MIC001',
            tipo: 'radial',
            status: 'em_uso',
            vida_util_km: 50000,
            data_fabricacao: '2023-01-15'
          },
          {
            id: 2,
            marca: 'Goodyear',
            modelo: 'KMAX D',
            numero_serie: 'GOO002',
            tipo: 'diagonal',
            status: 'estoque',
            vida_util_km: 60000,
            data_fabricacao: '2023-03-20'
          },
          {
            id: 3,
            marca: 'Pirelli',
            modelo: 'Formula Energy',
            numero_serie: 'PIR003',
            tipo: 'radial',
            status: 'manutencao',
            vida_util_km: 40000,
            data_fabricacao: '2022-11-01'
          }
        ]);
        setLoading(false);
      }, 500);
    } catch (error) {
      console.error('Erro ao carregar pneus:', error);
      setLoading(false);
    }
  };

  const handleOpenModal = (pneu = null) => {
    if (pneu) {
      setSelectedPneu(pneu);
      setFormData(pneu);
    } else {
      setSelectedPneu(null);
      setFormData({
        marca: '',
        modelo: '',
        numero_serie: '',
        tipo: 'radial',
        status: 'estoque',
        vida_util_km: 0,
        data_fabricacao: ''
      });
    }
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedPneu(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (selectedPneu) {
        setPneus(pneus.map(p => 
          p.id === selectedPneu.id ? { ...formData, id: selectedPneu.id } : p
        ));
      } else {
        const newPneu = { ...formData, id: Date.now() };
        setPneus([...pneus, newPneu]);
      }
      handleCloseModal();
    } catch (error) {
      console.error('Erro ao salvar pneu:', error);
    }
  };

  const handleDelete = async () => {
    try {
      setPneus(pneus.filter(p => p.id !== selectedPneu.id));
      setIsDeleteDialogOpen(false);
      setSelectedPneu(null);
    } catch (error) {
      console.error('Erro ao excluir pneu:', error);
    }
  };

  const filteredPneus = pneus.filter(pneu =>
    pneu.marca.toLowerCase().includes(searchTerm.toLowerCase()) ||
    pneu.modelo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    pneu.numero_serie.toLowerCase().includes(searchTerm.toLowerCase()) ||
    pneu.status.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Lista de Pneus</h1>
          <p className="text-white/70 mt-1">Gerencie todos os pneus da sua frota</p>
        </div>
        <button
          onClick={() => handleOpenModal()}
          className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg hover:from-green-700 hover:to-emerald-700 transition shadow-lg"
        >
          <Plus size={20} />
          Novo Pneu
        </button>
      </div>

      {/* Search Bar */}
      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
        <SearchBar 
          onSearch={setSearchTerm}
          placeholder="Buscar por marca, modelo, número de série ou status..."
        />
      </div>

      {/* Table */}
      <div className="bg-white/5 backdrop-blur-sm rounded-lg border border-white/10 overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center p-12">
            <div className="text-center">
              <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-white/20 border-t-white"></div>
              <p className="mt-4 text-white/70">Carregando pneus...</p>
            </div>
          </div>
        ) : filteredPneus.length === 0 ? (
          <div className="flex flex-col items-center justify-center p-12">
            <Gauge size={48} className="text-white/30 mb-4" />
            <p className="text-white/70 text-lg">Nenhum pneu encontrado</p>
            <p className="text-white/50 text-sm mt-2">Clique em "Novo Pneu" para cadastrar</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-white/10">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Marca</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Modelo</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Nº Série</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Tipo</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Status</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Vida Útil (KM)</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Fabricação</th>
                  <th className="px-6 py-4 text-right text-sm font-semibold text-white">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/10">
                {filteredPneus.map((pneu) => (
                  <tr key={pneu.id} className="hover:bg-white/5 transition">
                    <td className="px-6 py-4 text-white font-medium">{pneu.marca}</td>
                    <td className="px-6 py-4 text-white/80">{pneu.modelo}</td>
                    <td className="px-6 py-4 text-white/80">{pneu.numero_serie}</td>
                    <td className="px-6 py-4 text-white/80">{pneu.tipo}</td>
                    <td className="px-6 py-4">
                      <StatusBadge status={pneu.status} />
                    </td>
                    <td className="px-6 py-4 text-white/80">{pneu.vida_util_km}</td>
                    <td className="px-6 py-4 text-white/80">{pneu.data_fabricacao}</td>
                    <td className="px-6 py-4">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleOpenModal(pneu)}
                          className="p-2 hover:bg-blue-500/20 rounded-lg transition text-blue-400"
                          title="Editar"
                        >
                          <Edit size={18} />
                        </button>
                        <button
                          onClick={() => {
                            setSelectedPneu(pneu);
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
        title={selectedPneu ? 'Editar Pneu' : 'Novo Pneu'}
        size="md"
      >
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Marca *
            </label>
            <input
              type="text"
              value={formData.marca}
              onChange={(e) => setFormData({ ...formData, marca: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Modelo *
            </label>
            <input
              type="text"
              value={formData.modelo}
              onChange={(e) => setFormData({ ...formData, modelo: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Número de Série *
            </label>
            <input
              type="text"
              value={formData.numero_serie}
              onChange={(e) => setFormData({ ...formData, numero_serie: e.target.value })}
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
              <option value="radial">Radial</option>
              <option value="diagonal">Diagonal</option>
            </select>
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
              <option value="estoque">Em Estoque</option>
              <option value="em_uso">Em Uso</option>
              <option value="manutencao">Em Manutenção</option>
              <option value="descartado">Descartado</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Vida Útil Estimada (KM) *
            </label>
            <input
              type="number"
              value={formData.vida_util_km}
              onChange={(e) => setFormData({ ...formData, vida_util_km: parseInt(e.target.value) })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Data de Fabricação *
            </label>
            <input
              type="date"
              value={formData.data_fabricacao}
              onChange={(e) => setFormData({ ...formData, data_fabricacao: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              required
            />
          </div>
        </div>
      </FormModal>

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={isDeleteDialogOpen}
        onClose={() => setIsDeleteDialogOpen(false)}
        onConfirm={handleDelete}
        title="Excluir Pneu"
        message={`Tem certeza que deseja excluir o pneu "${selectedPneu?.marca} ${selectedPneu?.modelo}"? Esta ação não pode ser desfeita.`}
        confirmText="Excluir"
        variant="danger"
      />
    </div>
  );
}

