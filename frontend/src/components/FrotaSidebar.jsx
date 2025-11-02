import { Link, useLocation } from 'react-router-dom';
import { 
  Truck, 
  UserCheck, 
  MapPin, 
  Navigation,
  ArrowLeft,
  Gauge
} from 'lucide-react';

export default function FrotaSidebar() {
  const location = useLocation();

  const menuItems = [
    { 
      name: 'Visão Geral', 
      path: '/dashboard/frota-dashboard', 
      icon: Gauge,
      exact: true
    },
    { 
      name: 'Veículos', 
      path: '/dashboard/frota-dashboard/veiculos', 
      icon: Truck 
    },
    { 
      name: 'Motoristas', 
      path: '/dashboard/frota-dashboard/motoristas', 
      icon: UserCheck 
    },
    { 
      name: 'Posições', 
      path: '/dashboard/frota-dashboard/posicoes', 
      icon: MapPin 
    },
    { 
      name: 'Rastreamento', 
      path: '/dashboard/frota-dashboard/rastreamento', 
      icon: Navigation 
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
        <h2 className="text-xl font-bold text-white">Gestão de Frota</h2>
        <p className="text-white/60 text-sm mt-1">Controle completo da frota</p>
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

