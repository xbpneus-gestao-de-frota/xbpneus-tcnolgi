import { useParams, Link } from "react-router-dom";
import useTryFetch from "../../../hooks/useTryFetch";
import Loader from "../../../components/Loader";
import ErrorState from "../../../components/ErrorState";
export default function VehicleDetail(){
  const { id } = useParams();
  const CANDIDATES = [`/api/transportador/frota/veiculos/${id}/`,`/api/frota/veiculos/${id}/`,`/api/veiculos/${id}/`];
  const MOCK = () => ({ id, placa: "ABC1D23", modelo: "Cavalo Mecânico", km: 458200, motorista: "João Silva", pneus: [] });
  const { data, error, loading, simulated, usedEndpoint } = useTryFetch(CANDIDATES, { mock: MOCK });
  return (
    <section>
      <div className="flex items-baseline justify-between mb-3">
        <h2 className="text-xl font-bold">Veículo #{id}</h2>
        <div className="text-xs opacity-60">{usedEndpoint ? `Endpoint: ${usedEndpoint}` : simulated ? "Modo simulado" : ""}</div>
      </div>
      <Link to="/app/transportador/frota/veiculos" className="text-sm underline">Voltar</Link>
      {loading && <Loader />}
      {error && <ErrorState message="Falha ao carregar veículo." />}
      {!loading && !error && data && (
        <div className="mt-3 space-y-2">
          <div><b>Placa:</b> {data.placa}</div>
          <div><b>Modelo:</b> {data.modelo}</div>
          <div><b>KM:</b> {data.km}</div>
          <div><b>Motorista:</b> {data.motorista}</div>
        </div>
      )}
    </section>
  );
}
