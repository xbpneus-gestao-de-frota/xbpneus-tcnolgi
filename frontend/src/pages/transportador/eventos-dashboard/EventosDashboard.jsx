import { Link } from "react-router-dom";

export default function EventosDashboard() {
  const items = [["Eventos de Pneus", "/transportador/dashboard/eventos/pneus"], ["Eventos de Manutenção", "/transportador/dashboard/eventos/manutencao"], ["Alertas do Sistema", "/transportador/dashboard/eventos/alertas"], ["Logs", "/transportador/dashboard/eventos/logs"]];
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Dashboard — Eventos</h1>
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
