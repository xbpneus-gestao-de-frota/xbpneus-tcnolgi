import { Link, useParams } from "react-router-dom";
import { PILLARS } from "./PillarsConfig";

export default function PilarPage(){
  const { pillar } = useParams();
  const p = PILLARS.find(x => x.key === pillar);
  if (!p) return <div className="text-red-300">Pilar não encontrado.</div>;
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">{p.label}</h1>
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {p.subs.map(s => (
          <Link
            key={s.key}
            to={`/hub/${p.key}/${s.key}`}
            className="rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 p-4"
          >
            <div className="text-lg font-semibold">{s.label}</div>
            <div className="opacity-70 text-sm">Abrir {s.label}</div>
          </Link>
        ))}
      </div>
    </div>
  );
}
