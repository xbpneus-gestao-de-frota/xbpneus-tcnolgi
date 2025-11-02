import ActionGrid from "../../components/ActionGrid";
import PageHeader from "../../components/PageHeader";

export default function Relatorios() {
  const actions = [
    { label: "Relatórios de Frota", to: "frota", desc: "Visualize relatórios detalhados sobre sua frota." },
    { label: "Relatórios de Pneus", to: "pneus", desc: "Acompanhe o desempenho e custo dos seus pneus." },
    { label: "Relatórios de Estoque", to: "estoque", desc: "Obtenha insights sobre o inventário e movimentações." },
    { label: "Relatórios de Manutenção", to: "manutencao", desc: "Analise o histórico e custos de manutenção." },
    { label: "Relatórios Financeiros", to: "financeiro", desc: "Monitore a saúde financeira da sua operação." },
  ];

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <PageHeader
        title="Relatórios e Análises"
        subtitle="Acesse informações estratégicas para a tomada de decisão"
      />
      <div className="mt-8">
        <ActionGrid actions={actions} />
      </div>
    </div>
  );
}

