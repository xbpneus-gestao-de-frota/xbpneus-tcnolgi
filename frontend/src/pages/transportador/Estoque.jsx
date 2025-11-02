import ActionGrid from "../../components/ActionGrid";
import PageHeader from "../../components/PageHeader";

export default function Estoque() {
  const actions = [
    { label: "Movimentações", to: "movimentacoes", desc: "Visualize e gerencie todas as movimentações de estoque." },
    { label: "Itens de Estoque", to: "itens", desc: "Gerencie os itens disponíveis no seu estoque." },
    { label: "Entradas/Saídas", to: "entradas-saidas", desc: "Registre e acompanhe as entradas e saídas de produtos." },
    { label: "Relatórios de Estoque", to: "relatorios-estoque", desc: "Acesse relatórios detalhados sobre o seu estoque." },
  ];

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <PageHeader
        title="Gestão de Estoque"
        subtitle="Gerencie o inventário e as movimentações de produtos"
      />
      <div className="mt-8">
        <ActionGrid actions={actions} />
      </div>
    </div>
  );
}

