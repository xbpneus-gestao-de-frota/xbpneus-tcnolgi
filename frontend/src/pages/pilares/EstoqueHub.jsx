import SidebarPilares from "@/components/SidebarPilares";
import { Link } from "react-router-dom";

const CARDS = [];

export default function EstoqueHub() {
  return (
    <div className="min-h-screen bg-[#0b1220] text-[#e5e7eb] flex">
      <SidebarPilares />
      <main className="flex-1 p-6">
        <h1 className="text-2xl font-bold mb-4">Estoque</h1>
        <p className="opacity-80 mb-4">Escolha uma subfuncionalidade:</p>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {CARDS.map((c, i) => (
            <Link key={i} to={c.to} className="rounded-xl border border-white/10 bg-white/5 p-4 hover:bg-white/10 transition">
              <div className="text-lg font-semibold">{c.label}</div>
              <div className="text-sm opacity-70 break-all">{c.to}</div>
            </Link>
          ))}
        </div>
      </main>
    </div>
  );
}
