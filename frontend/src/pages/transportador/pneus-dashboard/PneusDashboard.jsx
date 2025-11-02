import { Link } from 'react-router-dom';
import {
  List,
  Plus,
  Target,
  ClipboardList,
  BarChart2,
  ShieldCheck,
  Gauge,
  Truck,
  AlertTriangle,
  CheckCircle
} from 'lucide-react';
import StatsCard from '../../../components/common/StatsCard';

export default function PneusDashboard() {
  const modules = [
    {
      title: 'Lista de Pneus',
      description: 'Visualizar e gerenciar todos os pneus cadastrados',
      icon: List,
      to: '/dashboard/pneus-dashboard/lista',
      color: 'blue',
      stats: '250'
    },
    {
      title: 'Cadastrar Pneu',
      description: 'Adicionar um novo pneu ao estoque',
      icon: Plus,
      to: '/dashboard/pneus-dashboard/cadastrar',
      color: 'green'
    },
    {
      title: 'Aplicações',
      description: 'Gerenciar a aplicação de pneus nos veículos',
      icon: Target,
      to: '/dashboard/pneus-dashboard/aplicacoes',
      color: 'purple'
    },
    {
      title: 'Manutenção Pneus',
      description: 'Registrar e acompanhar manutenções específicas de pneus',
      icon: ClipboardList,
      to: '/dashboard/pneus-dashboard/manutencao',
      color: 'orange'
    },
    {
      title: 'Análise de Desempenho',
      description: 'Analisar o desempenho e vida útil dos pneus',
      icon: BarChart2,
      to: '/dashboard/pneus-dashboard/analise',
      color: 'red'
    },
    {
      title: 'Garantias',
      description: 'Gerenciar garantias de pneus e recapagens',
      icon: ShieldCheck,
      to: '/dashboard/pneus-dashboard/garantias',
      color: 'indigo'
    }
  ];

  const stats = [
    {
      title: 'Total de Pneus',
      value: '250',
      icon: Gauge,
      trend: '+10',
      trendUp: true,
      color: 'blue'
    },
    {
      title: 'Pneus em Uso',
      value: '180',
      icon: Truck,
      trend: '+5',
      trendUp: true,
      color: 'green'
    },
    {
      title: 'Pneus em Estoque',
      value: '70',
      icon: CheckCircle,
      trend: '-2',
      trendUp: false,
      color: 'orange'
    },
    {
      title: 'Pneus com Alerta',
      value: '15',
      icon: AlertTriangle,
      trend: '+3',
      trendUp: true,
      color: 'red'
    }
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Gestão de Pneus</h1>
        <p className="text-white/70 text-lg">Controle completo do ciclo de vida dos pneus da sua frota</p>
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
      <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-bold text-white">Pneus Recentes</h3>
          <Link 
            to="/dashboard/pneus-dashboard/lista" 
            className="text-blue-400 hover:text-blue-300 text-sm font-medium"
          >
            Ver todos →
          </Link>
        </div>
        <div className="space-y-4">
          {[
            { id: 1, marca: 'Michelin', modelo: 'X MultiWay 3D', status: 'Em Uso', color: 'green' },
            { id: 2, marca: 'Goodyear', modelo: 'KMAX D', status: 'Estoque', color: 'orange' },
            { id: 3, marca: 'Pirelli', modelo: 'Formula Energy', status: 'Alerta', color: 'red' }
          ].map((pneu, index) => (
            <div key={index} className="flex items-center justify-between p-4 bg-white/5 rounded-lg hover:bg-white/10 transition">
              <div className="flex items-center gap-4">
                <div className="p-2 bg-blue-500/20 rounded-lg">
                  <Gauge size={20} className="text-blue-400" />
                </div>
                <div>
                  <p className="text-white font-medium">{pneu.marca} {pneu.modelo}</p>
                  <p className="text-white/60 text-sm">ID: {pneu.id}</p>
                </div>
              </div>
              <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                pneu.color === 'green' 
                  ? 'bg-green-500/20 text-green-400 border border-green-500/30' 
                  : pneu.color === 'orange'
                  ? 'bg-orange-500/20 text-orange-400 border border-orange-500/30'
                  : 'bg-red-500/20 text-red-400 border border-red-500/30'
              }`}>
                {pneu.status}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

