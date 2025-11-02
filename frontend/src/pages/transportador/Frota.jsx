import { Link } from "react-router-dom";
import PageHeader from "../../components/PageHeader";
import DataTable from "../../components/DataTable";
import Loader from "../../components/Loader";
import ErrorState from "../../components/ErrorState";
import useTryFetch from "../../hooks/useTryFetch";

export default function Frota() {
  // KPIs (contagens rápidas via DRF: usar page_size=1 para pegar meta.count)
  const veiculos = useTryFetch(
    ["/api/transportador/frota/veiculos/"],
    { paginated: true, params: { page_size: 1 } }
  );

  const posicoes = useTryFetch(
    ["/api/transportador/frota/posicoes/"],
    { paginated: true, params: { page_size: 1 } }
  );

  // Se houver endpoint de implementos no seu backend, ele entra aqui.
  // Mantemos como opcional; se não existir, o card simplesmente não aparece.
  const implementos = useTryFetch(
    [
      "/api/transportador/implemento/implementos/",
      "/api/transportador/frota/implementos/",
    ],
    { paginated: true, params: { page_size: 1 } }
  );

  // Recentes (últimos 5 veículos)
  const recentes = useTryFetch(
    ["/api/transportador/frota/veiculos/"],
    { paginated: true, params: { ordering: "-id", page_size: 5 } }
  );

  const kpi = (title, value, to, extra) => (
    <Link
      to={to}
      className="rounded-xl p-6 bg-white shadow-md hover:shadow-lg transition border border-gray-100"
    >
      <div className="text-sm text-gray-500">{title}</div>
      <div className="text-3xl font-extrabold">{value ?? 0}</div>
      {extra && <div className="mt-1 text-xs text-gray-400">{extra}</div>}
    </Link>
  );

  const totalVeiculos = veiculos?.meta?.count ?? 0;
  const totalPosicoes = posicoes?.meta?.count ?? 0;
  const totalImplementos =
    implementos?.meta?.count ?? (implementos?.data ? implementos.data.length : 0);

  const carregando =
    veiculos.loading || posicoes.loading || implementos.loading || recentes.loading;
  const erro = veiculos.error || posicoes.error || recentes.error;

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <PageHeader
        title="Gestão de Frota"
        subtitle="KPIs, ações rápidas e últimos veículos"
      >
        {veiculos.usedEndpoint && (
          <span className="text-xs text-gray-500">
            Veículos: {veiculos.usedEndpoint}
          </span>
        )}
      </PageHeader>

      {carregando && <Loader />}
      {erro && <ErrorState message="Falha ao carregar dados de Frota." />}

      {!carregando && !erro && (
        <>
          {/* KPIs */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {kpi("Total de Veículos", totalVeiculos, "/transportador/dashboard/frota/veiculos")}
            {kpi("Posições Mapeadas", totalPosicoes, "/transportador/dashboard/frota/posicoes")}
            {totalImplementos > 0 &&
              kpi("Implementos", totalImplementos, "/transportador/dashboard/frota/implementos")}
          </div>

          {/* Ações rápidas */}
          <div className="flex flex-wrap gap-3 mb-8">
            <Link
              to="/transportador/dashboard/frota/veiculos/create"
              className="px-5 py-3 rounded-lg bg-blue-600 text-white hover:bg-blue-700"
            >
              ➕ Novo Veículo
            </Link>
            <Link
              to="/transportador/dashboard/frota/posicoes"
              className="px-5 py-3 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700"
            >
              🗺️ Mapa de Posições
            </Link>
            <Link
              to="/transportador/dashboard/frota/motoristas"
              className="px-5 py-3 rounded-lg bg-emerald-600 text-white hover:bg-emerald-700"
            >
              👤 Motoristas
            </Link>
          </div>

          {/* Veículos recentes */}
          <div className="bg-white rounded-xl shadow-md p-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Veículos Recentes</h3>
              <Link
                to="/transportador/dashboard/frota/veiculos"
                className="text-sm text-blue-600 hover:underline"
              >
                Ver todos →
              </Link>
            </div>

            {recentes.data && recentes.data.length > 0 ? (
              <DataTable
                columns={[
                  { key: "id", label: "ID" },
                  { key: "placa", label: "Placa" },
                  { key: "modelo_veiculo_marca", label: "Marca" },
                  { key: "modelo_veiculo_nome", label: "Modelo" },
                  { key: "km", label: "KM" },
                ]}
                rows={recentes.data}
              />
            ) : (
              <div className="text-sm text-gray-500">Nenhum veículo recente encontrado.</div>
            )}
          </div>
        </>
      )}
    </div>
  );
}
