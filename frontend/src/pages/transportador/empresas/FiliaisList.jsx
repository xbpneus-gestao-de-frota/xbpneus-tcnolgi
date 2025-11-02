import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import useTryFetch from "../../../hooks/useTryFetch";
import DataTable from "../../../components/DataTable";
import ColumnPicker from "../../../components/ColumnPicker";
import Loader from "../../../components/Loader";
import ErrorState from "../../../components/ErrorState";
import EmptyState from "../../../components/EmptyState";
import PageHeader from "../../../components/PageHeader";
import api from "../../../api/http";

const CANDIDATES = ["/api/transportador/empresas/filiais/", "/api/filiais/"];

export default function FiliaisList() {
  const navigate = useNavigate();
  const [q, setQ] = useState("");
  const [ordering, setOrdering] = useState("codigo");
  const [deleting, setDeleting] = useState(null);
  const [empresa, setEmpresa] = useState("");
  const [ativa, setAtiva] = useState("");
  const [matriz, setMatriz] = useState("");

  const params = {};
  if (q) params.search = q;
  if (ordering) params.ordering = ordering;
  if (empresa) params.empresa = empresa;
  if (ativa !== "") params.ativa = ativa;
  if (matriz !== "") params.matriz = matriz;

  const { data, error, loading, usedEndpoint, meta, page, setPage } = useTryFetch(
    CANDIDATES,
    { params, paginated: true, initialPage: 1, pageSize: 20 }
  );

  // Buscar lista de empresas para o filtro
  const { data: empresas } = useTryFetch(["/api/transportador/empresas/empresas/"]);

  const handleDelete = async (id, nome) => {
    if (!confirm(`Tem certeza que deseja excluir a filial ${nome}?`)) return;

    setDeleting(id);
    try {
      await api.delete(`/api/transportador/empresas/filiais/${id}/`);
      window.location.reload();
    } catch (ex) {
      alert("Erro ao excluir filial.");
      console.error(ex);
    } finally {
      setDeleting(null);
    }
  };

  const handleToggleAtiva = async (id, ativaAtual) => {
    try {
      const action = ativaAtual ? "desativar" : "ativar";
      await api.post(`/api/transportador/empresas/filiais/${id}/${action}/`);
      window.location.reload();
    } catch (ex) {
      alert("Erro ao alterar status da filial.");
      console.error(ex);
    }
  };

  const handleDefinirMatriz = async (id) => {
    if (!confirm("Tem certeza que deseja definir esta filial como matriz?")) return;

    try {
      await api.post(`/api/transportador/empresas/filiais/${id}/definir_matriz/`);
      window.location.reload();
    } catch (ex) {
      alert("Erro ao definir filial como matriz.");
      console.error(ex);
    }
  };

  const cols = [
    { key: "id", label: "ID" },
    { key: "empresa_nome", label: "Empresa" },
    { key: "codigo", label: "Código" },
    { key: "nome", label: "Nome" },
    { key: "cidade", label: "Cidade" },
    { key: "estado", label: "Estado" },
    {
      key: "matriz",
      label: "Matriz",
      render: (row) => (
        <span
          className={`px-2 py-1 text-xs rounded ${
            row.matriz ? "bg-purple-100 text-purple-800" : "bg-gray-100 text-gray-800"
          }`}
        >
          {row.matriz ? "Sim" : "Não"}
        </span>
      ),
    },
    {
      key: "ativa",
      label: "Status",
      render: (row) => (
        <span
          className={`px-2 py-1 text-xs rounded ${
            row.ativa ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
          }`}
        >
          {row.ativa ? "Ativa" : "Inativa"}
        </span>
      ),
    },
    {
      key: "acoes",
      label: "Ações",
      render: (row) => (
        <div className="flex items-center gap-2">
          <button
            onClick={() => navigate(`/dashboard/filiais/${row.id}`)}
            className="px-3 py-1 text-sm rounded bg-blue-500 text-white hover:bg-blue-600"
          >
            Ver
          </button>
          <button
            onClick={() => navigate(`/dashboard/filiais/${row.id}/edit`)}
            className="px-3 py-1 text-sm rounded bg-green-500 text-white hover:bg-green-600"
          >
            Editar
          </button>
          {!row.matriz && (
            <button
              onClick={() => handleDefinirMatriz(row.id)}
              className="px-3 py-1 text-sm rounded bg-purple-500 text-white hover:bg-purple-600"
            >
              Definir Matriz
            </button>
          )}
          <button
            onClick={() => handleToggleAtiva(row.id, row.ativa)}
            className={`px-3 py-1 text-sm rounded text-white ${
              row.ativa ? "bg-orange-500 hover:bg-orange-600" : "bg-teal-500 hover:bg-teal-600"
            }`}
          >
            {row.ativa ? "Desativar" : "Ativar"}
          </button>
          <button
            onClick={() => handleDelete(row.id, row.nome)}
            disabled={deleting === row.id}
            className="px-3 py-1 text-sm rounded bg-red-500 text-white hover:bg-red-600 disabled:opacity-50"
          >
            {deleting === row.id ? "..." : "Excluir"}
          </button>
        </div>
      ),
    },
  ];

  const [selectedCols, setSelectedCols] = useState(cols.map((c) => c.label));
  useEffect(() => {
    try {
      const saved = localStorage.getItem("cols:" + window.location.pathname);
      if (saved) {
        setSelectedCols(JSON.parse(saved));
      }
    } catch {}
  }, []);

  const visibleCols = cols.filter((c) => selectedCols.includes(c.label));

  if (loading) return <Loader />;
  if (error) return <ErrorState error={error} />;

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="flex items-center justify-between mb-6">
        <PageHeader title="Filiais" subtitle="Gestão de filiais das empresas">
          {usedEndpoint && (
            <span className="text-xs text-gray-500">Endpoint: {usedEndpoint}</span>
          )}
        </PageHeader>
        <button
          onClick={() => navigate("/dashboard/filiais/new")}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          + Nova Filial
        </button>
      </div>

      {/* Filtros */}
      <div className="bg-white p-4 rounded shadow mb-4 grid grid-cols-1 md:grid-cols-5 gap-4">
        <input
          type="text"
          placeholder="Buscar..."
          value={q}
          onChange={(e) => setQ(e.target.value)}
          className="border px-3 py-2 rounded"
        />
        <select
          value={empresa}
          onChange={(e) => setEmpresa(e.target.value)}
          className="border px-3 py-2 rounded"
        >
          <option value="">Todas as empresas</option>
          {empresas &&
            empresas.map((emp) => (
              <option key={emp.id} value={emp.id}>
                {emp.nome}
              </option>
            ))}
        </select>
        <select
          value={ativa}
          onChange={(e) => setAtiva(e.target.value)}
          className="border px-3 py-2 rounded"
        >
          <option value="">Todos os status</option>
          <option value="true">Ativas</option>
          <option value="false">Inativas</option>
        </select>
        <select
          value={matriz}
          onChange={(e) => setMatriz(e.target.value)}
          className="border px-3 py-2 rounded"
        >
          <option value="">Todas</option>
          <option value="true">Apenas Matrizes</option>
          <option value="false">Apenas Filiais</option>
        </select>
        <ColumnPicker
          allCols={cols.map((c) => c.label)}
          selected={selectedCols}
          onChange={setSelectedCols}
        />
      </div>

      {/* Tabela */}
      {data && data.length === 0 ? (
        <EmptyState
          message="Nenhuma filial encontrada"
          action={() => navigate("/dashboard/filiais/new")}
          actionLabel="Criar primeira filial"
        />
      ) : (
        <DataTable
          data={data || []}
          columns={visibleCols}
          meta={meta}
          page={page}
          onPageChange={setPage}
        />
      )}
    </div>
  );
}

