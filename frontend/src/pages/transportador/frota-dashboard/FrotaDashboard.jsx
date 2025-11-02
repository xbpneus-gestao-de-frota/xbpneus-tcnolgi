import { Link } from 'react-router-dom';
import { 
  Truck, 
  UserCheck, 
  MapPin, 
  Navigation,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Layers
} from 'lucide-react';
import StatsCard from '../../../components/common/StatsCard';

export default function FrotaDashboard() {
  const modules = [
    {
      title: 'Veículos',
      description: 'Cadastro e gerenciamento da frota de veículos',
      icon: Truck,
      to: '/dashboard/frota-dashboard/veiculos',
      color: 'blue',
      stats: '45'
    },
    {
      title: 'Motoristas',
      description: 'Gestão de motoristas e habilitações',
      icon: UserCheck,
      to: '/dashboard/frota-dashboard/motoristas',
      color: 'green',
      stats: '78'
    },
    {
      title: 'Posições',
      description: 'Gerenciamento das posições dos pneus nos veículos',
      icon: Layers,
      to: '/dashboard/frota-dashboard/posicoes',
      color: 'purple',
      stats: '180'
    },
    {
      title: 'Rastreamento',
      description: 'Monitoramento e rastreamento em tempo real da frota',
      icon: Navigation,
      to: '/dashboard/frota-dashboard/rastreamento',
      color: 'indigo',
      stats: '42'
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
      title: 'Motoristas Ativos',
      value: '78',
      icon: UserCheck,
      trend: '+8',
      trendUp: true,
      color: 'green'
    },
    {
      title: 'Posições Ocupadas',
      value: '180',
      icon: MapPin,
      trend: '+15',
      trendUp: true,
      color: 'purple'
    },
    {
      title: 'Veículos Operando',
      value: '33',
      icon: CheckCircle,
      trend: '+2',
      trendUp: true,
      color: 'emerald'
    }
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Gestão de Frota</h1>
        <p className="text-white/70 text-lg">Controle completo de veículos, motoristas e operações</p>
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
        <h2 className="text-2xl font-bold text-white mb-6">Módulos Disponíveis</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {modules.map((module, index) => {
            const Icon = module.icon;
            const colorClasses = {
              blue: 'from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700',
              green: 'from-green-500 to-green-600 hover:from-green-600 hover:to-green-700',
              purple: 'from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700',
              orange: 'from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700',
              indigo: 'from-indigo-500 to-indigo-600 hover:from-indigo-600 hover:to-indigo-700'
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
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Veículos Recentes */}
        <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold text-white">Veículos Recentes</h3>
            <Link 
              to="/dashboard/frota-dashboard/veiculos" 
              className="text-blue-400 hover:text-blue-300 text-sm font-medium"
            >
              Ver todos →
            </Link>
          </div>
          <div className="space-y-4">
            {[
              { placa: 'ABC-1234', modelo: 'Scania R450', status: 'Operando', color: 'green' },
              { placa: 'DEF-5678', modelo: 'Volvo FH 540', status: 'Manutenção', color: 'orange' },
              { placa: 'GHI-9012', modelo: 'Mercedes Actros', status: 'Operando', color: 'green' }
            ].map((veiculo, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-white/5 rounded-lg hover:bg-white/10 transition">
                <div className="flex items-center gap-4">
                  <div className="p-2 bg-blue-500/20 rounded-lg">
                    <Truck size={20} className="text-blue-400" />
                  </div>
                  <div>
                    <p className="text-white font-medium">{veiculo.placa}</p>
                    <p className="text-white/60 text-sm">{veiculo.modelo}</p>
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

        {/* Atividades Recentes */}
        <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold text-white">Atividades Recentes</h3>
          </div>
          <div className="space-y-4">
            {[
              { 
                tipo: 'Novo Veículo', 
                descricao: 'ABC-1234 cadastrado', 
                tempo: 'Há 2 horas',
                icon: Truck,
                color: 'blue'
              },
              { 
                tipo: 'Manutenção', 
                descricao: 'OS #123 concluída', 
                tempo: 'Há 4 horas',
                icon: Wrench,
                color: 'orange'
              },
              { 
                tipo: 'Motorista', 
                descricao: 'João Silva habilitado', 
                tempo: 'Há 6 horas',
                icon: UserCheck,
                color: 'green'
              }
            ].map((atividade, index) => {
              const Icon = atividade.icon;
              return (
                <div key={index} className="flex items-start gap-4 p-4 bg-white/5 rounded-lg hover:bg-white/10 transition">
                  <div className={`p-2 bg-${atividade.color}-500/20 rounded-lg`}>
                    <Icon size={20} className={`text-${atividade.color}-400`} />
                  </div>
                  <div className="flex-1">
                    <p className="text-white font-medium">{atividade.tipo}</p>
                    <p className="text-white/60 text-sm">{atividade.descricao}</p>
                    <p className="text-white/40 text-xs mt-1">{atividade.tempo}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

