import { Link, useLocation } from "react-router-dom";

const PILARES = [
  {
    "slug": "frota",
    "label": "Frota"
  },
  {
    "slug": "pneus",
    "label": "Pneus"
  },
  {
    "slug": "estoque",
    "label": "Estoque"
  },
  {
    "slug": "manutencao",
    "label": "Manutencao"
  },
  {
    "slug": "motorista",
    "label": "Motorista"
  },
  {
    "slug": "ia",
    "label": "Ia"
  },
  {
    "slug": "configuracoes",
    "label": "Configuracoes"
  },
  {
    "slug": "borracharia",
    "label": "Borracharia"
  },
  {
    "slug": "revenda",
    "label": "Revenda"
  },
  {
    "slug": "recapagem",
    "label": "Recapagem"
  }
];

export default function SidebarPilares() {
  const loc = useLocation();
  return (
    <aside className="w-64 flex-shrink-0 border-r border-white/10 bg-white/5 p-4">
      <h2 className="text-sm font-semibold opacity-70 mb-2">Pilares</h2>
      <nav className="flex flex-col gap-1">
        {PILARES.map(p => (
          <Link
            key={p.slug}
            to={`/`+p.slug}
            className={`rounded-lg px-3 py-2 hover:bg-white/10 transition ${loc.pathname.startsWith('/'+p.slug) ? 'bg-white/10' : ''}`}
          >
            {p.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
