import { Link } from "react-router-dom";

export default function FinanceiroDashboard() {
  const items = [["Contas a Pagar", "/transportador/dashboard/financeiro/pagar"], ["Contas a Receber", "/transportador/dashboard/financeiro/receber"], ["Fluxo de Caixa", "/transportador/dashboard/financeiro/fluxo"], ["Centro de Custos", "/transportador/dashboard/financeiro/centros"]];
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Dashboard — Financeiro</h1>
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
