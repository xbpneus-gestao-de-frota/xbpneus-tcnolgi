import { Link } from 'react-router-dom';
import {
  List,
  Layers,
  Settings,
  MapPin,
  CheckCircle,
  AlertTriangle,
  Truck
} from 'lucide-react';
import StatsCard from '../../../../components/common/StatsCard';

export default function PosicoesDashboard() {
  const modules = [
    {
      title: 'Lista de Posições',
      description: 'Visualizar e gerenciar todas as posições de pneus',
      icon: List,
      to: '/dashboard/frota-dashboard/posicoes/lista',
      color: 'blue',
      stats: '180'
    },
    {
      title: 'Gerenciar Posições',
      description: 'Atribuir e desatribuir pneus às posições dos veículos',
      icon: Layers,
      to: '/dashboard/frota-dashboard/posicoes/gerenciar',
      color: 'green'
    },
    {
      title: 'Configurações',
      description: 'Configurar tipos de posições e veículos',
      icon: Settings,
      to: '/dashboard/frota-dashboard/posicoes/configuracoes',
      color: 'purple'
    }
  ];

  const stats = [
    {
      title: 'Total de Posições',
      value: '180',
      icon: MapPin,
      trend: '+10',
      trendUp: true,
      color: 'blue'
    },
    {
      title: 'Posições Ocupadas',
      value: '150',
      icon: CheckCircle,
      trend: '+5',
      trendUp: true,
      color: 'green'
    },
    {
      title: 'Posições Livres',
      value: '30',
      icon: AlertTriangle,
      trend: '-2',
      trendUp: false,
      color: 'orange'
    },
    {
      title: 'Veículos com Posições',
      value: '45',
      icon: Truck,
      trend: '+1',
      trendUp: true,
      color: 'purple'
    }
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Gestão de Posições</h1>
        <p className="text-white/70 text-lg">Controle das posições dos pneus nos veículos</p>
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
          <h3 className="text-xl font-bold text-white">Posições Recentes</h3>
          <Link 
            to="/dashboard/frota-dashboard/posicoes/lista" 
            className="text-blue-400 hover:text-blue-300 text-sm font-medium"
          >
            Ver todas →
          </Link>
        </div>
        <div className="space-y-4">
          {[
            { veiculo: 'ABC-1234', posicao: 'Eixo 1, Posição 1', pneu: 'Pneu 123', status: 'Ocupada', color: 'green' },
            { veiculo: 'DEF-5678', posicao: 'Eixo 2, Posição 3', pneu: 'Pneu 456', status: 'Ocupada', color: 'green' },
            { veiculo: 'GHI-9012', posicao: 'Eixo 3, Posição 2', pneu: 'Livre', status: 'Livre', color: 'orange' }
          ].map((pos, index) => (
            <div key={index} className="flex items-center justify-between p-4 bg-white/5 rounded-lg hover:bg-white/10 transition">
              <div className="flex items-center gap-4">
                <div className="p-2 bg-blue-500/20 rounded-lg">
                  <MapPin size={20} className="text-blue-400" />
                </div>
                <div>
                  <p className="text-white font-medium">{pos.posicao}</p>
                  <p className="text-white/60 text-sm">Veículo: {pos.veiculo} • Pneu: {pos.pneu}</p>
                </div>
              </div>
              <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                pos.color === 'green' 
                  ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                  : 'bg-orange-500/20 text-orange-400 border border-orange-500/30'
              }`}>
                {pos.status}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

