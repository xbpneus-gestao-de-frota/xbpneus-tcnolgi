import { Link } from 'react-router-dom';
import {
  Gauge,
  Wrench,
  ClipboardList,
  AlertTriangle,
  CheckCircle,
  CalendarCheck,
  Hourglass
} from 'lucide-react';
import StatsCard from '../../../components/common/StatsCard';

export default function ManutencaoDashboard() {
  const modules = [
    {
      title: 'Ordens de Serviço',
      description: 'Gerenciar todas as ordens de serviço abertas e concluídas',
      icon: Wrench,
      to: '/dashboard/manutencao-dashboard/ordens-servico',
      color: 'blue',
      stats: '15'
    },
    {
      title: 'Testes Pós-Manutenção',
      description: 'Registrar e acompanhar testes realizados após manutenções',
      icon: CheckCircle,
      to: '/dashboard/manutencao-dashboard/testes',
      color: 'green'
    },
    {
      title: 'Relatórios',
      description: 'Gerar relatórios de manutenção e desempenho da frota',
      icon: ClipboardList,
      to: '/dashboard/manutencao-dashboard/relatorios',
      color: 'purple'
    },
    {
      title: 'Configurações',
      description: 'Configurar tipos de manutenção, checklists e alertas',
      icon: Settings,
      to: '/dashboard/manutencao-dashboard/configuracoes',
      color: 'orange'
    }
  ];

  const stats = [
    {
      title: 'OS Abertas',
      value: '15',
      icon: Wrench,
      trend: '+3 esta semana',
      trendUp: true,
      color: 'blue'
    },
    {
      title: 'OS Concluídas (mês)',
      value: '45',
      icon: CheckCircle,
      trend: '+10% em relação ao mês anterior',
      trendUp: true,
      color: 'green'
    },
    {
      title: 'Próximas Manutenções',
      value: '8',
      icon: CalendarCheck,
      trend: '2 veículos com manutenção urgente',
      trendUp: false,
      color: 'orange'
    },
    {
      title: 'Tempo Médio de OS',
      value: '2.5 dias',
      icon: Hourglass,
      trend: '-0.5 dias',
      trendUp: false,
      color: 'emerald'
    }
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Gestão de Manutenção</h1>
        <p className="text-white/70 text-lg">Controle completo de ordens de serviço, testes e planejamento</p>
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
              red: 'from-red-500 to-red-600 hover:from-red-600 hover:to-red-700',
              emerald: 'from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700'
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
          <h3 className="text-xl font-bold text-white">Últimas Ordens de Serviço</h3>
          <Link 
            to="/dashboard/manutencao-dashboard/ordens-servico" 
            className="text-blue-400 hover:text-blue-300 text-sm font-medium"
          >
            Ver todas →
          </Link>
        </div>
        <div className="space-y-4">
          {[
            { id: 1, veiculo: 'ABC-1234', tipo: 'Preventiva', status: 'Em Andamento', data: '2025-10-14', color: 'blue' },
            { id: 2, veiculo: 'DEF-5678', tipo: 'Corretiva', status: 'Concluída', data: '2025-10-13', color: 'green' },
            { id: 3, veiculo: 'GHI-9012', tipo: 'Preditiva', status: 'Pendente', data: '2025-10-12', color: 'orange' }
          ].map((os, index) => (
            <div key={index} className="flex items-center justify-between p-4 bg-white/5 rounded-lg hover:bg-white/10 transition">
              <div className="flex items-center gap-4">
                <div className={`p-2 bg-${os.color}-500/20 rounded-lg`}>
                  <Wrench size={20} className={`text-${os.color}-400`} />
                </div>
                <div>
                  <p className="text-white font-medium">OS {os.veiculo}: {os.tipo}</p>
                  <p className="text-white/60 text-sm">Status: {os.status} - {os.data}</p>
                </div>
              </div>
              <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                os.status === 'Concluída' 
                  ? 'bg-green-500/20 text-green-400 border border-green-500/30' 
                  : os.status === 'Em Andamento' 
                  ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                  : 'bg-orange-500/20 text-orange-400 border border-orange-500/30'
              }`}>
                {os.status}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

