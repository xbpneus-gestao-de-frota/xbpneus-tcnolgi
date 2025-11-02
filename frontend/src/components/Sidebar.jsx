import { NavLink } from "react-router-dom";
import { TRANSPORTADOR_MENU_ROUTES } from "@/config/transportadorNavigation";
import { transportadorPath } from "@/config/transportadorPaths";

export default function Sidebar() {
  const items = TRANSPORTADOR_MENU_ROUTES.map(({ path, label, icon, highlight, index }) => ({
    to: index ? transportadorPath() : transportadorPath(path),
    label,
    Icon: icon,
    highlight: Boolean(highlight),
  }));

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
          const Icon = it.Icon;
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

