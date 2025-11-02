import { useState } from "react";
import { useNavigate } from "react-router-dom";
import useTryFetch from "../../../hooks/useTryFetch";
import DataTable from "../../../components/DataTable";
import Loader from "../../../components/Loader";
import ErrorState from "../../../components/ErrorState";
import PageHeader from "../../../components/PageHeader";
import api from "../../../api/http";

const CANDIDATES = ["/api/transportador/manutencao/ordens/"];

export default function OSList(){
  const navigate = useNavigate();
  const [status, setStatus] = useState("");
  const [tipo, setTipo] = useState("");
  const params = {};
  if (status) params.status = status;
  if (tipo) params.tipo = tipo;
  const { data, error, loading, meta, page, setPage } = useTryFetch(CANDIDATES, { params, paginated: true, pageSize: 20 });

  const cols = [
    {"key": "numero", "label": "Número"},
    {"key": "veiculo_placa", "label": "Veículo"},
    {"key": "tipo", "label": "Tipo"},
    {"key": "status", "label": "Status"},
    {"key": "prioridade", "label": "Prioridade"},
    {"key": "data_abertura", "label": "Abertura"},
    {"key": "custo_total", "label": "Custo Total"},
    {
      "key": "acoes",
      "label": "Ações",
      "render": (row) => (
        <div className="flex gap-2">
          <button onClick={() => navigate(`/dashboard/manutencao/os/${row.id}`)} className="px-3 py-1 text-sm rounded bg-blue-500 text-white hover:bg-blue-600">Ver</button>
          <button onClick={() => navigate(`/dashboard/manutencao/os/${row.id}/edit`)} className="px-3 py-1 text-sm rounded bg-green-500 text-white hover:bg-green-600">Editar</button>
        </div>
      )
    }
  ];

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="flex items-center justify-between mb-6">
        <PageHeader title="Ordens de Serviço" subtitle="Gestão de manutenções" />
        <button onClick={() => navigate("/dashboard/manutencao/os/create")} className="px-6 py-3 rounded-lg bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 text-white font-medium hover:opacity-90 flex items-center gap-2">
          <span className="text-xl">+</span>Nova OS
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-md p-4 mb-6">
        <div className="flex gap-3">
          <select value={status} onChange={e=>setStatus(e.target.value)} className="px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="">Todos os status</option>
            <option value="ABERTA">Aberta</option>
            <option value="AGENDADA">Agendada</option>
            <option value="EM_ANDAMENTO">Em Andamento</option>
            <option value="CONCLUIDA">Concluída</option>
          </select>
          <select value={tipo} onChange={e=>setTipo(e.target.value)} className="px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="">Todos os tipos</option>
            <option value="PREVENTIVA">Preventiva</option>
            <option value="CORRETIVA">Corretiva</option>
            <option value="EMERGENCIAL">Emergencial</option>
          </select>
        </div>
      </div>

      {loading && <Loader />}
      {error && <ErrorState message="Falha ao carregar ordens de serviço." />}
      {!loading && !error && data && <DataTable columns={cols} rows={data} />}
    </div>
  );
}
