import ActionGrid from "../../components/ActionGrid";
import PageHeader from "../../components/PageHeader";

export default function Manutencao() {
  const actions = [
    { label: "Ordens de Serviço", to: "os", desc: "Gerencie as ordens de serviço da sua frota." },
    { label: "Testes Pós-Manutenção", to: "testes-pos-manutencao", desc: "Registre e acompanhe os testes realizados após as manutenções." },
    { label: "Histórico de Manutenção", to: "historico", desc: "Visualize o histórico completo de manutenção de cada veículo." },
    { label: "Planejamento Preventivo", to: "planejamento-preventivo", desc: "Crie e gerencie planos de manutenção preventiva para sua frota." },
  ];

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <PageHeader
        title="Gestão de Manutenção"
        subtitle="Gerencie as ordens de serviço, testes e histórico de manutenção da sua frota"
      />
      <div className="mt-8">
        <ActionGrid actions={actions} />
      </div>
    </div>
  );
}

