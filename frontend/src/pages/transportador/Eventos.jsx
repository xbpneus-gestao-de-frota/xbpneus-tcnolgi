import { useState, useEffect } from "react";
import api from "../../api/http";
import PageHeader from "../../components/PageHeader";
import Loader from "../../components/Loader";
import ErrorState from "../../components/ErrorState";

export default function Eventos() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filtro, setFiltro] = useState("todos");
  const [eventos, setEventos] = useState([
    {
      id: 1,
      tipo: "manutencao",
      titulo: "Manutenção Preventiva Realizada",
      descricao: "Manutenção preventiva realizada no veículo ABC-1234",
      data: "2025-10-18T14:30:00",
      icone: "🔧",
      cor: "yellow"
    },
    {
      id: 2,
      tipo: "alerta",
      titulo: "Alerta de Pressão de Pneu",
      descricao: "Pressão baixa detectada no pneu frontal esquerdo do veículo XYZ-5678",
      data: "2025-10-18T10:15:00",
      icone: "⚠️",
      cor: "red"
    },
    {
      id: 3,
      tipo: "compra",
      titulo: "Compra de Pneus Realizada",
      descricao: "Compra de 4 pneus Michelin para reposição de frota",
      data: "2025-10-17T16:45:00",
      icone: "🛒",
      cor: "blue"
    },
    {
      id: 4,
      tipo: "manutencao",
      titulo: "Ordem de Serviço Concluída",
      descricao: "OS #1234 concluída com sucesso - Troca de óleo e filtro",
      data: "2025-10-17T11:20:00",
      icone: "✅",
      cor: "green"
    },
    {
      id: 5,
      tipo: "alerta",
      titulo: "Limite de Quilometragem Próximo",
      descricao: "Veículo ABC-1234 atingiu 95% da quilometragem para próxima manutenção",
      data: "2025-10-16T09:00:00",
      icone: "📊",
      cor: "orange"
    },
    {
      id: 6,
      tipo: "sistema",
      titulo: "Sincronização de Dados Concluída",
      descricao: "Sincronização de dados com servidor concluída com sucesso",
      data: "2025-10-16T00:30:00",
      icone: "🔄",
      cor: "purple"
    },
    {
      id: 7,
      tipo: "compra",
      titulo: "Pedido Entregue",
      descricao: "Pedido de peças de reposição entregue com sucesso",
      data: "2025-10-15T14:00:00",
      icone: "📦",
      cor: "blue"
    },
    {
      id: 8,
      tipo: "manutencao",
      titulo: "Inspeção de Segurança Realizada",
      descricao: "Inspeção de segurança do veículo DEF-9012 realizada",
      data: "2025-10-15T10:30:00",
      icone: "🛡️",
      cor: "green"
    }
  ]);

  useEffect(() => {
    setLoading(false);
  }, []);

  const eventosFiltrados = filtro === "todos"
    ? eventos
    : eventos.filter(e => e.tipo === filtro);

  const formatarData = (dataString) => {
    const data = new Date(dataString);
    const hoje = new Date();
    const ontem = new Date(hoje);
    ontem.setDate(ontem.getDate() - 1);

    if (data.toDateString() === hoje.toDateString()) {
      return `Hoje às ${data.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" })}`;
    } else if (data.toDateString() === ontem.toDateString()) {
      return `Ontem às ${data.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" })}`;
    } else {
      return data.toLocaleDateString("pt-BR", { year: "numeric", month: "short", day: "numeric" });
    }
  };

  const getCorFundo = (cor) => {
    const cores = {
      yellow: "bg-yellow-50 border-yellow-200",
      red: "bg-red-50 border-red-200",
      blue: "bg-blue-50 border-blue-200",
      green: "bg-green-50 border-green-200",
      orange: "bg-orange-50 border-orange-200",
      purple: "bg-purple-50 border-purple-200"
    };
    return cores[cor] || cores.blue;
  };

  const getCorTexto = (cor) => {
    const cores = {
      yellow: "text-yellow-800",
      red: "text-red-800",
      blue: "text-blue-800",
      green: "text-green-800",
      orange: "text-orange-800",
      purple: "text-purple-800"
    };
    return cores[cor] || cores.blue;
  };

  if (loading) return <Loader />;
  if (error) return <ErrorState message={error} />;

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <PageHeader 
        title="Eventos" 
        subtitle="Registro de todos os eventos e atividades do sistema"
      />

      {/* Filtros */}
      <div className="bg-white rounded-xl shadow-md p-6 mb-8">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Filtrar por Tipo</h2>
        <div className="flex gap-4 flex-wrap">
          {["todos", "manutencao", "alerta", "compra", "sistema"].map((tipo) => (
            <button
              key={tipo}
              onClick={() => setFiltro(tipo)}
              className={`px-6 py-2 rounded-lg font-medium transition-colors ${
                filtro === tipo
                  ? "bg-blue-500 text-white"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              {tipo === "todos" ? "Todos" : tipo.charAt(0).toUpperCase() + tipo.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Timeline de Eventos */}
      <div className="space-y-4">
        {eventosFiltrados.length === 0 ? (
          <div className="bg-white rounded-xl shadow-md p-8 text-center">
            <p className="text-gray-600 text-lg">Nenhum evento encontrado para este filtro</p>
          </div>
        ) : (
          eventosFiltrados.map((evento, index) => (
            <div
              key={evento.id}
              className={`bg-white rounded-xl shadow-md p-6 border-l-4 hover:shadow-lg transition-shadow ${
                getCorFundo(evento.cor)
              }`}
            >
              <div className="flex items-start gap-4">
                {/* Ícone */}
                <div className="text-4xl flex-shrink-0">{evento.icone}</div>

                {/* Conteúdo */}
                <div className="flex-grow">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className={`text-lg font-semibold ${getCorTexto(evento.cor)}`}>
                      {evento.titulo}
                    </h3>
                    <span className="text-xs text-gray-500 ml-4 flex-shrink-0">
                      {formatarData(evento.data)}
                    </span>
                  </div>
                  <p className="text-gray-600">{evento.descricao}</p>

                  {/* Tags */}
                  <div className="mt-3 flex gap-2">
                    <span className={`text-xs px-3 py-1 rounded-full font-medium ${
                      evento.tipo === "manutencao" ? "bg-yellow-100 text-yellow-800" :
                      evento.tipo === "alerta" ? "bg-red-100 text-red-800" :
                      evento.tipo === "compra" ? "bg-blue-100 text-blue-800" :
                      evento.tipo === "sistema" ? "bg-purple-100 text-purple-800" :
                      "bg-gray-100 text-gray-800"
                    }`}>
                      {evento.tipo === "manutencao" ? "🔧 Manutenção" :
                       evento.tipo === "alerta" ? "⚠️ Alerta" :
                       evento.tipo === "compra" ? "🛒 Compra" :
                       evento.tipo === "sistema" ? "⚙️ Sistema" :
                       "📌 Outro"}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Estatísticas */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-xl shadow-md p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-600">Total de Eventos</span>
            <span className="text-2xl">📊</span>
          </div>
          <div className="text-2xl font-bold text-blue-600">{eventos.length}</div>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-600">Manutenções</span>
            <span className="text-2xl">🔧</span>
          </div>
          <div className="text-2xl font-bold text-yellow-600">{eventos.filter(e => e.tipo === "manutencao").length}</div>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-600">Alertas</span>
            <span className="text-2xl">⚠️</span>
          </div>
          <div className="text-2xl font-bold text-red-600">{eventos.filter(e => e.tipo === "alerta").length}</div>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-600">Compras</span>
            <span className="text-2xl">🛒</span>
          </div>
          <div className="text-2xl font-bold text-blue-600">{eventos.filter(e => e.tipo === "compra").length}</div>
        </div>
      </div>

      {/* Ações */}
      <div className="mt-8 bg-white rounded-xl shadow-md p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Ações</h2>
        <div className="flex gap-4 flex-wrap">
          <button className="px-6 py-2 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 transition-colors">
            📥 Exportar Eventos
          </button>
          <button className="px-6 py-2 bg-green-500 text-white rounded-lg font-medium hover:bg-green-600 transition-colors">
            🔔 Configurar Notificações
          </button>
          <button className="px-6 py-2 bg-purple-500 text-white rounded-lg font-medium hover:bg-purple-600 transition-colors">
            📋 Gerar Relatório
          </button>
        </div>
      </div>
    </div>
  );
}

