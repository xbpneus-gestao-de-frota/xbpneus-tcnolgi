import { NavLink } from "react-router-dom";
import { 
  Home, 
  Truck, 
  Circle, 
  Package, 
  Wrench, 
  Brain, 
  DollarSign, 
  ShoppingCart, 
  Calendar, 
  FileText, 
  Settings,
  Building2,
  MapPin
} from 'lucide-react';

const items = [
  { to: "/transportador/dashboard", label: "Início", icon: Home },
  { to: "/transportador/dashboard/frota", label: "Frota", icon: Truck },
  { to: "/transportador/dashboard/pneus", label: "Pneus", icon: Circle },
  { to: "/transportador/dashboard/estoque", label: "Estoque", icon: Package },
  { to: "/transportador/dashboard/manutencao", label: "Manutenção", icon: Wrench },
  { to: "/transportador/dashboard/ia", label: "IA - Análise", icon: Brain, highlight: true },
  { to: "/transportador/dashboard/financeiro", label: "Financeiro", icon: DollarSign },
  { to: "/transportador/dashboard/compras", label: "Compras", icon: ShoppingCart },
  { to: "/transportador/dashboard/eventos", label: "Eventos", icon: Calendar },
  { to: "/transportador/dashboard/relatorios", label: "Relatórios", icon: FileText },
  { to: "/transportador/dashboard/configuracoes", label: "Configurações", icon: Settings },
  { to: "/transportador/dashboard/empresas", label: "Empresas", icon: Building2 },
  { to: "/transportador/dashboard/filiais", label: "Filiais", icon: MapPin },
];

export default function Sidebar() {
  return (
    <aside className="w-60 shrink-0 bg-[#1A237E] text-white shadow-lg">
      {/* Logo com degradê */}
      <div 
        className="p-4 font-black text-2xl text-center border-b border-white/20"
        style={{
          background: 'linear-gradient(135deg, #60a5fa, #6366f1, #7c3aed)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          letterSpacing: '0.05em',
        }}
      >
        XBPNEUS
      </div>
      
      {/* Menu de navegação */}
      <nav className="p-2 space-y-1">
        {items.map(it => {
          const Icon = it.icon;
          return (
            <NavLink 
              key={it.to} 
              to={it.to} 
              className={({isActive}) => 
                "flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 " + 
                (isActive 
                  ? "bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 text-white font-semibold shadow-md" 
                  : "hover:bg-[#3949AB] text-white/90"
                ) +
                (it.highlight ? " font-bold border-2 border-blue-400/50" : "")
              }
            >
              <Icon size={20} />
              <span>{it.label}</span>
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}

