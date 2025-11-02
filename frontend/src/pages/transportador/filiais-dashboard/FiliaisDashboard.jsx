import { Link } from "react-router-dom";

export default function FiliaisDashboard() {
  const items = [["Filiais", "/transportador/dashboard/filiais"], ["Empresas", "/transportador/dashboard/empresas"]];
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Dashboard — Filiais</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {items.map(([label, to]) => (
          <Link
            key={to}
            to={to}
            className="rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 p-4 transition flex items-center justify-between"
          >
            <span>{label}</span>
            <span className="opacity-60">→</span>
          </Link>
        ))}
      </div>
    </div>
  );
}
