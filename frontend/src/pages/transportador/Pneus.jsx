import ActionGrid from "../../components/ActionGrid";
import PageHeader from "../../components/PageHeader";

export default function Pneus() {
  const actions = [
    { label: "Lista de Pneus", to: "lista", desc: "Visualize e gerencie todos os pneus da sua frota." },
    { label: "Aplicações", to: "aplicacoes", desc: "Acompanhe a aplicação e o histórico de uso dos pneus." },
    { label: "Manutenção de Pneus", to: "manutencao-pneus", desc: "Gerencie a manutenção preventiva e corretiva dos seus pneus." },
    { label: "Análise de Desgaste", to: "analise-desgaste", desc: "Analise o desgaste dos pneus para otimizar a vida útil." },
    { label: "Garantias", to: "garantias", desc: "Gerencie as garantias dos seus pneus e acione-as quando necessário." },
    { label: "Eventos de Pneus", to: "eventos-pneus", desc: "Registre e acompanhe todos os eventos relacionados aos pneus." },
  ];

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <PageHeader
        title="Gestão de Pneus"
        subtitle="Gerencie o ciclo de vida dos pneus da sua frota"
      />
      <div className="mt-8">
        <ActionGrid actions={actions} />
      </div>
    </div>
  );
}

