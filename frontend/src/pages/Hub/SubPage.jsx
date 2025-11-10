import { Link, useParams } from "react-router-dom";
import { PILLARS } from "./PillarsConfig";

// Mapa opcional: se existir uma rota real já implementada, criamos um atalho
const KNOWN_MAP = {
  "manutencao:ordens-servico": "/manutencao/ordens-servico",
  "manutencao:os-criar": "/manutencao/ordens-servico/create",
  "manutencao:testes-pos-manutencao": "/manutencao/testes-pos-manutencao",
  "manutencao:planejamento-preventivo": "/manutencao/planejamento-preventivo",
  "ia:analise": "/ia/analise",
  "ia:gamificacao": "/ia/gamificacao",
  "ia:garantias": "/ia/garantias",
  "estoque:entradas": "/estoque/entradas",
  "estoque:saidas": "/estoque/saidas",
  "estoque:inventario": "/estoque/inventario"
};

export default function SubPage(){
  const { pillar, sub } = useParams();
  const p = PILLARS.find(x => x.key === pillar);
  const s = p?.subs.find(x => x.key === sub);
  const key = `${pillar}:${sub}`;
  const real = KNOWN_MAP[key];

  return (
    <div>
      <h1 className="text-2xl font-bold mb-2">{p?.label} ▸ {s?.label || sub}</h1>
      <p className="opacity-80 mb-4">
        Esta é uma tela placeholder para a subfuncionalidade. Substitua por sua implementação.
      </p>
      <div className="flex gap-3">
        {real && (
          <Link
            to={real}
            className="px-4 py-2 rounded-lg border border-white/10 bg-white/5 hover:bg-white/10"
          >
            Abrir módulo existente
          </Link>
        )}
        <Link
          to={`/hub/${pillar}`}
          className="px-4 py-2 rounded-lg border border-white/10 hover:bg-white/10"
        >
          Voltar
        </Link>
      </div>
    </div>
  );
}
