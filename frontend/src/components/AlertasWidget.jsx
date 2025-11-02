import React, { useState, useEffect } from 'react';
import api from '../api/http';

const AlertasWidget = () => {
  const [alertas, setAlertas] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAlertas();
  }, []);

  const fetchAlertas = async () => {
    try {
      const [pneus, veiculos] = await Promise.all([
        api.get('/api/transportador/pneus/pneus/'),
        api.get('/api/transportador/frota/veiculos/')
      ]);

      const alertasGerados = [];

      // Alertas de pneus críticos (sulco < 3mm)
      pneus.data.forEach(pneu => {
        if (pneu.sulco_atual && pneu.sulco_atual < 3) {
          alertasGerados.push({
            tipo: 'CRITICO',
            titulo: 'Pneu Crítico',
            mensagem: `Pneu ${pneu.numero_fogo} com sulco ${pneu.sulco_atual}mm - TROCAR URGENTE!`,
            acao: `/dashboard/pneus/${pneu.id}`
          });
        } else if (pneu.sulco_atual && pneu.sulco_atual < 5) {
          alertasGerados.push({
            tipo: 'ALERTA',
            titulo: 'Pneu em Atenção',
            mensagem: `Pneu ${pneu.numero_fogo} com sulco ${pneu.sulco_atual}mm - Considere recapagem`,
            acao: `/dashboard/pneus/${pneu.id}`
          });
        }
      });

      // Alertas de manutenção (KM próximo)
      veiculos.data.forEach(veiculo => {
        if (veiculo.km_atual && veiculo.km_proxima_manutencao) {
          const kmRestante = veiculo.km_proxima_manutencao - veiculo.km_atual;
          if (kmRestante < 1000 && kmRestante > 0) {
            alertasGerados.push({
              tipo: 'ALERTA',
              titulo: 'Manutenção Próxima',
              mensagem: `Veículo ${veiculo.placa} - Faltam ${kmRestante}km para manutenção`,
              acao: `/dashboard/frota/veiculos/${veiculo.id}`
            });
          } else if (kmRestante <= 0) {
            alertasGerados.push({
              tipo: 'CRITICO',
              titulo: 'Manutenção Atrasada',
              mensagem: `Veículo ${veiculo.placa} - Manutenção ATRASADA em ${Math.abs(kmRestante)}km!`,
              acao: `/dashboard/manutencao/ordens-servico/create`
            });
          }
        }
      });

      setAlertas(alertasGerados.slice(0, 5)); // Mostrar apenas 5 alertas
    } catch (err) {
      console.error('Erro ao carregar alertas:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return null;
  if (alertas.length === 0) return null;

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
      <div className="flex items-center gap-2 mb-4">
        <span className="text-2xl">⚠️</span>
        <h2 className="text-xl font-bold text-gray-800">Alertas Importantes</h2>
      </div>

      <div className="space-y-3">
        {alertas.map((alerta, index) => (
          <div
            key={index}
            className={`p-4 rounded-lg border-l-4 ${
              alerta.tipo === 'CRITICO'
                ? 'bg-red-50 border-red-500'
                : 'bg-yellow-50 border-yellow-500'
            }`}
          >
            <div className="flex justify-between items-start">
              <div>
                <h3 className={`font-semibold ${
                  alerta.tipo === 'CRITICO' ? 'text-red-700' : 'text-yellow-700'
                }`}>
                  {alerta.titulo}
                </h3>
                <p className="text-sm text-gray-600 mt-1">{alerta.mensagem}</p>
              </div>
              {alerta.acao && (
                <a
                  href={alerta.acao}
                  className="text-sm text-blue-600 hover:text-blue-800 font-medium"
                >
                  Ver →
                </a>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AlertasWidget;
