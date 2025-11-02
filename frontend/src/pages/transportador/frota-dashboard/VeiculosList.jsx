import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Truck, Eye, FileText } from 'lucide-react';
import { Link } from 'react-router-dom';
import FormModal from '../../../components/common/FormModal';
import ConfirmDialog from '../../../components/common/ConfirmDialog';
import StatusBadge from '../../../components/common/StatusBadge';
import SearchBar from '../../../components/common/SearchBar';

export default function VeiculosList() {
  const [veiculos, setVeiculos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [selectedVeiculo, setSelectedVeiculo] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState({
    placa: '',
    modelo: '',
    marca: '',
    ano_fabricacao: '',
    ano_modelo: '',
    chassi: '',
    renavam: '',
    cor: '',
    tipo: '',
    capacidade_carga: '',
    km_atual: '',
    data_aquisicao: '',
    valor_aquisicao: '',
    status: 'ativo'
  });

  useEffect(() => {
    fetchVeiculos();
  }, []);

  const fetchVeiculos = async () => {
    setLoading(true);
    try {
      setTimeout(() => {
        setVeiculos([
          {
            id: 1,
            placa: 'ABC-1234',
            modelo: 'Scania R450',
            marca: 'Scania',
            ano_fabricacao: '2022',
            ano_modelo: '2023',
            tipo: 'Cavalo Mecânico',
            km_atual: '45000',
            status: 'ativo'
          },
          {
            id: 2,
            placa: 'DEF-5678',
            modelo: 'Volvo FH 540',
            marca: 'Volvo',
            ano_fabricacao: '2021',
            ano_modelo: '2022',
            tipo: 'Cavalo Mecânico',
            km_atual: '78000',
            status: 'manutencao'
          },
          {
            id: 3,
            placa: 'GHI-9012',
            modelo: 'Mercedes Actros 2651',
            marca: 'Mercedes-Benz',
            ano_fabricacao: '2023',
            ano_modelo: '2023',
            tipo: 'Cavalo Mecânico',
            km_atual: '12000',
            status: 'ativo'
          }
        ]);
        setLoading(false);
      }, 500);
    } catch (error) {
      console.error('Erro ao carregar veículos:', error);
      setLoading(false);
    }
  };

  const handleOpenModal = (veiculo = null) => {
    if (veiculo) {
      setSelectedVeiculo(veiculo);
      setFormData(veiculo);
    } else {
      setSelectedVeiculo(null);
      setFormData({
        placa: '',
        modelo: '',
        marca: '',
        ano_fabricacao: '',
        ano_modelo: '',
        chassi: '',
        renavam: '',
        cor: '',
        tipo: '',
        capacidade_carga: '',
        km_atual: '',
        data_aquisicao: '',
        valor_aquisicao: '',
        status: 'ativo'
      });
    }
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedVeiculo(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (selectedVeiculo) {
        setVeiculos(veiculos.map(veic => 
          veic.id === selectedVeiculo.id ? { ...formData, id: selectedVeiculo.id } : veic
        ));
      } else {
        const newVeiculo = { ...formData, id: Date.now() };
        setVeiculos([...veiculos, newVeiculo]);
      }
      handleCloseModal();
    } catch (error) {
      console.error('Erro ao salvar veículo:', error);
    }
  };

  const handleDelete = async () => {
    try {
      setVeiculos(veiculos.filter(veic => veic.id !== selectedVeiculo.id));
      setIsDeleteDialogOpen(false);
      setSelectedVeiculo(null);
    } catch (error) {
      console.error('Erro ao excluir veículo:', error);
    }
  };

  const filteredVeiculos = veiculos.filter(veiculo =>
    veiculo.placa.toLowerCase().includes(searchTerm.toLowerCase()) ||
    veiculo.modelo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    veiculo.marca.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Veículos</h1>
          <p className="text-white/70 mt-1">Gerencie a frota de veículos</p>
        </div>
        <button
          onClick={() => handleOpenModal()}
          className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-lg hover:from-blue-700 hover:to-indigo-700 transition shadow-lg"
        >
          <Plus size={20} />
          Novo Veículo
        </button>
      </div>

      {/* Search Bar */}
      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
        <SearchBar 
          onSearch={setSearchTerm}
          placeholder="Buscar por placa, modelo ou marca..."
        />
      </div>

      {/* Table */}
      <div className="bg-white/5 backdrop-blur-sm rounded-lg border border-white/10 overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center p-12">
            <div className="text-center">
              <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-white/20 border-t-white"></div>
              <p className="mt-4 text-white/70">Carregando veículos...</p>
            </div>
          </div>
        ) : filteredVeiculos.length === 0 ? (
          <div className="flex flex-col items-center justify-center p-12">
            <Truck size={48} className="text-white/30 mb-4" />
            <p className="text-white/70 text-lg">Nenhum veículo encontrado</p>
            <p className="text-white/50 text-sm mt-2">Clique em "Novo Veículo" para cadastrar</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-white/10">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Placa</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Modelo</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Marca</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Ano</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Tipo</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">KM Atual</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-white">Status</th>
                  <th className="px-6 py-4 text-right text-sm font-semibold text-white">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/10">
                {filteredVeiculos.map((veiculo) => (
                  <tr key={veiculo.id} className="hover:bg-white/5 transition">
                    <td className="px-6 py-4">
                      <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-500/20 text-blue-300 border border-blue-500/30">
                        {veiculo.placa}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-white font-medium">{veiculo.modelo}</td>
                    <td className="px-6 py-4 text-white/80">{veiculo.marca}</td>
                    <td className="px-6 py-4 text-white/80">{veiculo.ano_fabricacao}/{veiculo.ano_modelo}</td>
                    <td className="px-6 py-4 text-white/80">{veiculo.tipo}</td>
                    <td className="px-6 py-4 text-white/80">{parseInt(veiculo.km_atual).toLocaleString('pt-BR')} km</td>
                    <td className="px-6 py-4">
                      <StatusBadge status={veiculo.status} />
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center justify-end gap-2">
                        <Link
                          to={`/dashboard/frota/veiculos/${veiculo.id}`}
                          className="p-2 hover:bg-green-500/20 rounded-lg transition text-green-400"
                          title="Visualizar"
                        >
                          <Eye size={18} />
                        </Link>
                        <button
                          onClick={() => handleOpenModal(veiculo)}
                          className="p-2 hover:bg-blue-500/20 rounded-lg transition text-blue-400"
                          title="Editar"
                        >
                          <Edit size={18} />
                        </button>
                        <button
                          onClick={() => {
                            setSelectedVeiculo(veiculo);
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
        title={selectedVeiculo ? 'Editar Veículo' : 'Novo Veículo'}
        size="xl"
      >
        <div className="space-y-6">
          {/* Dados Básicos */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4 pb-2 border-b">Dados Básicos</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Placa *
                </label>
                <input
                  type="text"
                  value={formData.placa}
                  onChange={(e) => setFormData({ ...formData, placa: e.target.value.toUpperCase() })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="ABC-1234"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Marca *
                </label>
                <input
                  type="text"
                  value={formData.marca}
                  onChange={(e) => setFormData({ ...formData, marca: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Modelo *
                </label>
                <input
                  type="text"
                  value={formData.modelo}
                  onChange={(e) => setFormData({ ...formData, modelo: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Ano Fabricação *
                </label>
                <input
                  type="number"
                  value={formData.ano_fabricacao}
                  onChange={(e) => setFormData({ ...formData, ano_fabricacao: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  min="1900"
                  max="2099"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Ano Modelo *
                </label>
                <input
                  type="number"
                  value={formData.ano_modelo}
                  onChange={(e) => setFormData({ ...formData, ano_modelo: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  min="1900"
                  max="2099"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Chassi
                </label>
                <input
                  type="text"
                  value={formData.chassi}
                  onChange={(e) => setFormData({ ...formData, chassi: e.target.value.toUpperCase() })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  RENAVAM
                </label>
                <input
                  type="text"
                  value={formData.renavam}
                  onChange={(e) => setFormData({ ...formData, renavam: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Cor
                </label>
                <input
                  type="text"
                  value={formData.cor}
                  onChange={(e) => setFormData({ ...formData, cor: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
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
                  <option value="">Selecione...</option>
                  <option value="Cavalo Mecânico">Cavalo Mecânico</option>
                  <option value="Caminhão Toco">Caminhão Toco</option>
                  <option value="Caminhão Truck">Caminhão Truck</option>
                  <option value="Carreta">Carreta</option>
                  <option value="Bitrem">Bitrem</option>
                  <option value="Rodotrem">Rodotrem</option>
                </select>
              </div>
            </div>
          </div>

          {/* Dados Operacionais */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4 pb-2 border-b">Dados Operacionais</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Capacidade de Carga (kg)
                </label>
                <input
                  type="number"
                  value={formData.capacidade_carga}
                  onChange={(e) => setFormData({ ...formData, capacidade_carga: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  KM Atual *
                </label>
                <input
                  type="number"
                  value={formData.km_atual}
                  onChange={(e) => setFormData({ ...formData, km_atual: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Data de Aquisição
                </label>
                <input
                  type="date"
                  value={formData.data_aquisicao}
                  onChange={(e) => setFormData({ ...formData, data_aquisicao: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Valor de Aquisição (R$)
                </label>
                <input
                  type="number"
                  value={formData.valor_aquisicao}
                  onChange={(e) => setFormData({ ...formData, valor_aquisicao: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  step="0.01"
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
                  <option value="manutencao">Em Manutenção</option>
                  <option value="inativo">Inativo</option>
                  <option value="vendido">Vendido</option>
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
        title="Excluir Veículo"
        message={`Tem certeza que deseja excluir o veículo "${selectedVeiculo?.placa}"? Esta ação não pode ser desfeita.`}
        confirmText="Excluir"
        variant="danger"
      />
    </div>
  );
}

