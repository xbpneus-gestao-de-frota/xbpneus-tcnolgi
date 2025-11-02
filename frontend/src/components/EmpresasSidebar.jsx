import { NavLink } from "react-router-dom";
import { 
  Building2, 
  MapPin, 
  Users, 
  FileText,
  Settings,
  BarChart3,
  ArrowLeft
} from 'lucide-react';

const items = [
  { to: "/dashboard/empresas-dashboard", label: "Visão Geral", icon: BarChart3, end: true },
  { to: "/dashboard/empresas-dashboard/empresas", label: "Empresas", icon: Building2 },
  { to: "/dashboard/empresas-dashboard/filiais", label: "Filiais", icon: MapPin },
  { to: "/dashboard/empresas-dashboard/agregados", label: "Agregados", icon: Users },
  { to: "/dashboard/empresas-dashboard/documentos", label: "Documentos", icon: FileText },
  { to: "/dashboard/empresas-dashboard/configuracoes", label: "Configurações", icon: Settings },
];

export default function EmpresasSidebar() {
  return (
    <aside className="w-60 shrink-0 bg-[#1A237E] text-white shadow-lg">
      {/* Header com botão voltar */}
      <div className="p-4 border-b border-white/20">
        <NavLink 
          to="/dashboard"
          className="flex items-center gap-2 text-white/90 hover:text-white transition mb-3"
        >
          <ArrowLeft size={20} />
          <span className="text-sm">Voltar ao Dashboard</span>
        </NavLink>
        <div 
          className="font-black text-xl text-center"
          style={{
            background: 'linear-gradient(135deg, #60a5fa, #6366f1, #7c3aed)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            letterSpacing: '0.05em',
          }}
        >
          GESTÃO DE EMPRESAS
        </div>
      </div>
      
      {/* Menu de navegação */}
      <nav className="p-2 space-y-1">
        {items.map(it => {
          const Icon = it.icon;
          return (
            <NavLink 
              key={it.to} 
              to={it.to}
              end={it.end}
              className={({isActive}) => 
                "flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 " + 
                (isActive 
                  ? "bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 text-white font-semibold shadow-md" 
                  : "hover:bg-[#3949AB] text-white/90"
                )
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

