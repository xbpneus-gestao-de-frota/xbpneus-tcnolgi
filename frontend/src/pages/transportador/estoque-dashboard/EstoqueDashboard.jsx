import { Link } from 'react-router-dom';
import {
  Gauge,
  Package,
  Truck,
  ClipboardList,
  History,
  AlertTriangle,
  CheckCircle
} from 'lucide-react';
import StatsCard from '../../../components/common/StatsCard';

export default function EstoqueDashboard() {
  const modules = [
    {
      title: 'Movimentações',
      description: 'Visualizar e gerenciar todas as entradas e saídas do estoque',
      icon: History,
      to: '/dashboard/estoque-dashboard/movimentacoes',
      color: 'blue',
      stats: '120'
    },
    {
      title: 'Itens em Estoque',
      description: 'Consultar o inventário atual de todos os itens',
      icon: Package,
      to: '/dashboard/estoque-dashboard/itens',
      color: 'green',
      stats: '500'
    },
    {
      title: 'Entradas',
      description: 'Registrar a entrada de novos itens no estoque',
      icon: Truck,
      to: '/dashboard/estoque-dashboard/entradas',
      color: 'purple'
    },
    {
      title: 'Saídas',
      description: 'Registrar a saída de itens do estoque',
      icon: Truck,
      to: '/dashboard/estoque-dashboard/saidas',
      color: 'orange'
    },
    {
      title: 'Relatórios',
      description: 'Gerar relatórios de estoque e movimentações',
      icon: ClipboardList,
      to: '/dashboard/estoque-dashboard/relatorios',
      color: 'red'
    }
  ];

  const stats = [
    {
      title: 'Total de Itens',
      value: '500',
      icon: Package,
      trend: '+20 este mês',
      trendUp: true,
      color: 'blue'
    },
    {
      title: 'Movimentações (últimos 30 dias)',
      value: '120',
      icon: History,
      trend: '+10% este mês',
      trendUp: true,
      color: 'green'
    },
    {
      title: 'Itens com Baixo Estoque',
      value: '15',
      icon: AlertTriangle,
      trend: '+3',
      trendUp: true,
      color: 'orange'
    },
    {
      title: 'Estoque Consistente',
      value: '98%',
      icon: CheckCircle,
      trend: '+0.5%',
      trendUp: true,
      color: 'emerald'
    }
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Gestão de Estoque</h1>
        <p className="text-white/70 text-lg">Controle completo de itens, entradas e saídas do seu estoque</p>
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
          <h3 className="text-xl font-bold text-white">Últimas Movimentações</h3>
          <Link 
            to="/dashboard/estoque-dashboard/movimentacoes" 
            className="text-blue-400 hover:text-blue-300 text-sm font-medium"
          >
            Ver todas →
          </Link>
        </div>
        <div className="space-y-4">
          {[
            { id: 1, tipo: 'Entrada', item: 'Pneu Michelin X', quantidade: 10, data: '2025-10-14', color: 'green' },
            { id: 2, tipo: 'Saída', item: 'Óleo Lubrificante', quantidade: 2, data: '2025-10-13', color: 'red' },
            { id: 3, tipo: 'Entrada', item: 'Filtro de Ar', quantidade: 5, data: '2025-10-12', color: 'green' }
          ].map((mov, index) => (
            <div key={index} className="flex items-center justify-between p-4 bg-white/5 rounded-lg hover:bg-white/10 transition">
              <div className="flex items-center gap-4">
                <div className={`p-2 bg-${mov.color}-500/20 rounded-lg`}>
                  {mov.tipo === 'Entrada' ? <Plus size={20} className={`text-${mov.color}-400`} /> : <Truck size={20} className={`text-${mov.color}-400`} />}
                </div>
                <div>
                  <p className="text-white font-medium">{mov.tipo}: {mov.item}</p>
                  <p className="text-white/60 text-sm">Qtd: {mov.quantidade} - {mov.data}</p>
                </div>
              </div>
              <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                mov.color === 'green' 
                  ? 'bg-green-500/20 text-green-400 border border-green-500/30' 
                  : 'bg-red-500/20 text-red-400 border border-red-500/30'
              }`}>
                {mov.tipo}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

