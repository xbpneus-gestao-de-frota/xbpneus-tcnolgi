import { Link, useLocation } from 'react-router-dom';
import {
  Gauge,
  List,
  Plus,
  Settings,
  ArrowLeft,
  Target,
  ClipboardList,
  BarChart2,
  ShieldCheck
} from 'lucide-react';

export default function PneusSidebar() {
  const location = useLocation();

  const menuItems = [
    {
      name: 'Visão Geral',
      path: '/dashboard/pneus-dashboard',
      icon: Gauge,
      exact: true
    },
    {
      name: 'Lista de Pneus',
      path: '/dashboard/pneus-dashboard/lista',
      icon: List
    },
    {
      name: 'Cadastrar Pneu',
      path: '/dashboard/pneus-dashboard/cadastrar',
      icon: Plus
    },
    {
      name: 'Aplicações',
      path: '/dashboard/pneus-dashboard/aplicacoes',
      icon: Target
    },
    {
      name: 'Manutenção Pneus',
      path: '/dashboard/pneus-dashboard/manutencao',
      icon: ClipboardList
    },
    {
      name: 'Análise de Desempenho',
      path: '/dashboard/pneus-dashboard/analise',
      icon: BarChart2
    },
    {
      name: 'Garantias',
      path: '/dashboard/pneus-dashboard/garantias',
      icon: ShieldCheck
    },
    {
      name: 'Configurações',
      path: '/dashboard/pneus-dashboard/configuracoes',
      icon: Settings
    }
  ];

  const isActive = (item) => {
    if (item.exact) {
      return location.pathname === item.path;
    }
    return location.pathname.startsWith(item.path);
  };

  return (
    <div className="w-64 bg-[#1A237E] min-h-screen fixed left-0 top-0 pt-20 shadow-xl z-40">
      {/* Header */}
      <div className="px-6 py-4 border-b border-white/10">
        <h2 className="text-xl font-bold text-white">Gestão de Pneus</h2>
        <p className="text-white/60 text-sm mt-1">Controle completo de pneus</p>
      </div>

      {/* Menu Items */}
      <nav className="mt-6 px-3">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item);
          
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`
                flex items-center gap-3 px-4 py-3 rounded-lg mb-2 transition-all duration-200
                ${active 
                  ? 'bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 text-white shadow-lg' 
                  : 'text-white/70 hover:bg-[#3949AB] hover:text-white'
                }
              `}
            >
              <Icon size={20} />
              <span className="font-medium">{item.name}</span>
            </Link>
          );
        })}
      </nav>

      {/* Back Button */}
      <div className="absolute bottom-6 left-0 right-0 px-3">
        <Link
          to="/dashboard"
          className="flex items-center gap-3 px-4 py-3 rounded-lg text-white/70 hover:bg-[#3949AB] hover:text-white transition-all duration-200"
        >
          <ArrowLeft size={20} />
          <span className="font-medium">Voltar ao Dashboard</span>
        </Link>
      </div>
    </div>
  );
}

