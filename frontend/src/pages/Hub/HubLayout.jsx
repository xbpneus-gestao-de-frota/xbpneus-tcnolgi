import { NavLink, Outlet } from "react-router-dom";
import { PILLARS } from "./PillarsConfig";

export default function HubLayout(){
  return (
    <div className="min-h-screen bg-[#0b1220] text-[#e5e7eb] flex">
      <aside className="w-64 border-r border-white/10 p-4">
        <h2 className="text-sm uppercase opacity-70 mb-3">Funcionalidades</h2>
        <nav className="flex flex-col gap-1">
          {PILLARS.map(p => (
            <NavLink
              key={p.key}
              to={`/hub/${p.key}`}
              className={({ isActive }) =>
                `px-3 py-2 rounded-lg hover:bg-white/10 ${isActive ? "bg-white/10" : ""}`
              }
            >
              {p.label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="flex-1 p-6">
        <Outlet />
      </main>
    </div>
  );
}
