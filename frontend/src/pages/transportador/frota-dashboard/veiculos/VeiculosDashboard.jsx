import { Link } from 'react-router-dom';
import { 
  List,
  Plus,
  Link as LinkIcon,
  FileText,
  Truck,
  CheckCircle,
  AlertTriangle,
  Wrench
} from 'lucide-react';
import StatsCard from '../../../../components/common/StatsCard';

export default function VeiculosDashboard() {
  const modules = [
    {
      title: 'Lista de Veículos',
      description: 'Visualizar todos os veículos cadastrados',
      icon: List,
      to: '/dashboard/frota-dashboard/veiculos/lista',
      color: 'blue',
      stats: '45'
    },
    {
      title: 'Inserir Veículo',
      description: 'Cadastrar novo veículo na frota',
      icon: Plus,
      to: '/dashboard/frota-dashboard/veiculos/inserir',
      color: 'green'
    },
    {
      title: 'Adicionar Implemento',
      description: 'Vincular implementos aos veículos',
      icon: LinkIcon,
      to: '/dashboard/frota-dashboard/veiculos/implemento',
      color: 'purple'
    },
    {
      title: 'Documentos',
      description: 'Gerenciar documentos dos veículos',
      icon: FileText,
      to: '/dashboard/frota-dashboard/veiculos/documentos',
      color: 'orange'
    }
  ];

  const stats = [
    {
      title: 'Total de Veículos',
      value: '45',
      icon: Truck,
      trend: '+5',
      trendUp: true,
      color: 'blue'
    },
    {
      title: 'Veículos Ativos',
      value: '33',
      icon: CheckCircle,
      trend: '+2',
      trendUp: true,
      color: 'green'
    },
    {
      title: 'Em Manutenção',
      value: '8',
      icon: Wrench,
      trend: '-3',
      trendUp: false,
      color: 'orange'
    },
    {
      title: 'Alertas',
      value: '4',
      icon: AlertTriangle,
      trend: '0',
      trendUp: false,
      color: 'red'
    }
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Gestão de Veículos</h1>
        <p className="text-white/70 text-lg">Controle completo da frota de veículos</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <StatsCard
            key={index}
            title={stat.title}
            value={stat.value}
            icon={stat.icon}
            trend={stat.trend}
            trendUp={stat.trendUp}
            color={stat.color}
          />
        ))}
      </div>

      {/* Module Cards */}
      <div>
        <h2 className="text-2xl font-bold text-white mb-6">Funcionalidades</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {modules.map((module, index) => {
            const Icon = module.icon;
            const colorClasses = {
              blue: 'from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700',
              green: 'from-green-500 to-green-600 hover:from-green-600 hover:to-green-700',
              purple: 'from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700',
              orange: 'from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700'
            };

            return (
              <Link
                key={index}
                to={module.to}
                className={`
                  bg-gradient-to-br ${colorClasses[module.color]}
                  rounded-xl p-6 shadow-lg hover:shadow-2xl transform hover:scale-105 transition-all duration-300
                  border border-white/10
                `}
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="p-3 bg-white/20 rounded-lg backdrop-blur-sm">
                    <Icon size={32} className="text-white" />
                  </div>
                  {module.stats && (
                    <div className="px-3 py-1 bg-white/20 rounded-full backdrop-blur-sm">
                      <span className="text-white font-bold text-sm">{module.stats}</span>
                    </div>
                  )}
                </div>
                <h3 className="text-xl font-bold text-white mb-2">{module.title}</h3>
                <p className="text-white/80 text-sm">{module.description}</p>
              </Link>
            );
          })}
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-bold text-white">Veículos Recentes</h3>
          <Link 
            to="/dashboard/frota-dashboard/veiculos/lista" 
            className="text-blue-400 hover:text-blue-300 text-sm font-medium"
          >
            Ver todos →
          </Link>
        </div>
        <div className="space-y-4">
          {[
            { placa: 'ABC-1234', modelo: 'Scania R450', status: 'Operando', color: 'green', km: '45.000' },
            { placa: 'DEF-5678', modelo: 'Volvo FH 540', status: 'Manutenção', color: 'orange', km: '78.000' },
            { placa: 'GHI-9012', modelo: 'Mercedes Actros', status: 'Operando', color: 'green', km: '12.000' }
          ].map((veiculo, index) => (
            <div key={index} className="flex items-center justify-between p-4 bg-white/5 rounded-lg hover:bg-white/10 transition">
              <div className="flex items-center gap-4">
                <div className="p-2 bg-blue-500/20 rounded-lg">
                  <Truck size={20} className="text-blue-400" />
                </div>
                <div>
                  <p className="text-white font-medium">{veiculo.placa}</p>
                  <p className="text-white/60 text-sm">{veiculo.modelo} • {veiculo.km} km</p>
                </div>
              </div>
              <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                veiculo.color === 'green' 
                  ? 'bg-green-500/20 text-green-400 border border-green-500/30' 
                  : 'bg-orange-500/20 text-orange-400 border border-orange-500/30'
              }`}>
                {veiculo.status}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

