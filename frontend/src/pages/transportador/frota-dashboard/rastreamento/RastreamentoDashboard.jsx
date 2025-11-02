import { Link } from 'react-router-dom';
import {
  MapPin,
  Truck,
  History,
  Settings,
  Gauge,
  CheckCircle,
  AlertTriangle
} from 'lucide-react';
import StatsCard from '../../../../components/common/StatsCard';

export default function RastreamentoDashboard() {
  const modules = [
    {
      title: 'Monitoramento Ao Vivo',
      description: 'Visualize a localização em tempo real da sua frota',
      icon: MapPin,
      to: '/dashboard/frota-dashboard/rastreamento/monitoramento',
      color: 'blue',
    },
    {
      title: 'Histórico de Rotas',
      description: 'Acompanhe o trajeto percorrido pelos veículos',
      icon: History,
      to: '/dashboard/frota-dashboard/rastreamento/historico',
      color: 'green',
    },
    {
      title: 'Veículos Rastreáveis',
      description: 'Gerencie quais veículos estão sendo rastreados',
      icon: Truck,
      to: '/dashboard/frota-dashboard/rastreamento/veiculos',
      color: 'purple',
    },
    {
      title: 'Configurações',
      description: 'Ajuste as configurações de rastreamento e alertas',
      icon: Settings,
      to: '/dashboard/frota-dashboard/rastreamento/configuracoes',
      color: 'orange',
    },
  ];

  const stats = [
    {
      title: 'Veículos Online',
      value: '38',
      icon: CheckCircle,
      trend: '+3',
      trendUp: true,
      color: 'green',
    },
    {
      title: 'Veículos Offline',
      value: '7',
      icon: AlertTriangle,
      trend: '-1',
      trendUp: false,
      color: 'red',
    },
    {
      title: 'Alertas Ativos',
      value: '5',
      icon: AlertTriangle,
      trend: '+2',
      trendUp: true,
      color: 'orange',
    },
    {
      title: 'Média de Rotas/Dia',
      value: '15',
      icon: History,
      trend: '+1',
      trendUp: true,
      color: 'blue',
    },
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Rastreamento de Frota</h1>
        <p className="text-white/70 text-lg">Monitore e gerencie sua frota em tempo real</p>
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
              orange: 'from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700',
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
          <h3 className="text-xl font-bold text-white">Eventos Recentes</h3>
          <Link 
            to="/dashboard/frota-dashboard/rastreamento/historico" 
            className="text-blue-400 hover:text-blue-300 text-sm font-medium"
          >
            Ver todos →
          </Link>
        </div>
        <div className="space-y-4">
          {[
            { veiculo: 'ABC-1234', evento: 'Entrou em área de risco', tempo: 'Há 5 min', icon: AlertTriangle, color: 'red' },
            { veiculo: 'DEF-5678', evento: 'Iniciou nova rota', tempo: 'Há 15 min', icon: History, color: 'green' },
            { veiculo: 'GHI-9012', evento: 'Parada não programada', tempo: 'Há 30 min', icon: MapPin, color: 'orange' }
          ].map((evento, index) => {
            const Icon = evento.icon;
            return (
              <div key={index} className="flex items-center justify-between p-4 bg-white/5 rounded-lg hover:bg-white/10 transition">
                <div className="flex items-center gap-4">
                  <div className={`p-2 bg-${evento.color}-500/20 rounded-lg`}>
                    <Icon size={20} className={`text-${evento.color}-400`} />
                  </div>
                  <div>
                    <p className="text-white font-medium">{evento.evento}</p>
                    <p className="text-white/60 text-sm">Veículo: {evento.veiculo} • {evento.tempo}</p>
                  </div>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                  evento.color === 'red' 
                    ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                    : evento.color === 'green'
                    ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                    : 'bg-orange-500/20 text-orange-400 border border-orange-500/30'
                }`}>
                  {evento.evento.includes('risco') ? 'Alerta' : 'Normal'}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

