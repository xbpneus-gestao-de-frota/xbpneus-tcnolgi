import React, { useState, useEffect } from 'react';
import api from '../../api/http';
import PageHeader from '../../components/PageHeader';

const Economia = () => {
  const [dados, setDados] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    calcularEconomia();
  }, []);

  const calcularEconomia = async () => {
    try {
      const [veiculos, pneus] = await Promise.all([
        api.get('/api/transportador/frota/veiculos/'),
        api.get('/api/transportador/pneus/pneus/')
      ]);

      const totalVeiculos = veiculos.data.length;
      const totalPneus = pneus.data.length;
      
      // Cálculos estimados
      const custoMedioPneu = 2400; // R$ por pneu novo
      const economiaPorPneu = custoMedioPneu * 0.4; // 40% economia com gestão
      const economiaTotal = totalPneus * economiaPorPneu;
      const economiaMensal = economiaTotal / 12;
      
      // Impacto ambiental
      const pneusSalvos = Math.floor(totalPneus * 0.3); // 30% menos descarte
      const co2Evitado = pneusSalvos * 100; // 100kg CO2 por pneu

      setDados({
        totalVeiculos,
        totalPneus,
        economiaTotal,
        economiaMensal,
        pneusSalvos,
        co2Evitado
      });
    } catch (err) {
      console.error('Erro:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-6">Carregando...</div>;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-6">
      <PageHeader 
        title="Economia e Impacto" 
        subtitle="Veja quanto você está economizando e ajudando o planeta"
      />

      <div className="max-w-6xl mx-auto mt-6 space-y-6">
        {/* Economia Financeira */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
            💰 Economia Financeira
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center p-6 bg-green-50 rounded-lg">
              <div className="text-4xl font-bold text-green-600">
                R$ {dados?.economiaTotal.toLocaleString('pt-BR')}
              </div>
              <div className="text-sm text-gray-600 mt-2">Economia Anual Estimada</div>
            </div>
            <div className="text-center p-6 bg-blue-50 rounded-lg">
              <div className="text-4xl font-bold text-blue-600">
                R$ {dados?.economiaMensal.toLocaleString('pt-BR')}
              </div>
              <div className="text-sm text-gray-600 mt-2">Economia Mensal</div>
            </div>
            <div className="text-center p-6 bg-purple-50 rounded-lg">
              <div className="text-4xl font-bold text-purple-600">
                {dados?.totalPneus}
              </div>
              <div className="text-sm text-gray-600 mt-2">Pneus Gerenciados</div>
            </div>
          </div>
        </div>

        {/* Impacto Ambiental */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
            🌍 Impacto Ambiental
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="text-center p-6 bg-green-50 rounded-lg">
              <div className="text-4xl font-bold text-green-600">
                {dados?.pneusSalvos}
              </div>
              <div className="text-sm text-gray-600 mt-2">Pneus Salvos do Descarte/Ano</div>
            </div>
            <div className="text-center p-6 bg-blue-50 rounded-lg">
              <div className="text-4xl font-bold text-blue-600">
                {dados?.co2Evitado} kg
              </div>
              <div className="text-sm text-gray-600 mt-2">CO₂ Evitado/Ano</div>
            </div>
          </div>
        </div>

        {/* Como Funciona */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            📊 Como Calculamos
          </h2>
          <div className="space-y-4 text-gray-700">
            <p>
              <strong>Economia Financeira:</strong> Baseado em gestão eficiente que aumenta a vida útil dos pneus em 40% através de rodízio correto, calibragem adequada e manutenção preventiva.
            </p>
            <p>
              <strong>Pneus Salvos:</strong> Com controle de sulco e recapagem no momento certo, evitamos 30% de descartes prematuros.
            </p>
            <p>
              <strong>CO₂ Evitado:</strong> Cada pneu fabricado gera ~100kg de CO₂. Ao prolongar a vida útil e recapar, reduzimos drasticamente a produção de novos pneus.
            </p>
          </div>
        </div>

        {/* Call to Action */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl shadow-lg p-8 text-white text-center">
          <h2 className="text-3xl font-bold mb-4">
            Faça a Diferença! 🌍
          </h2>
          <p className="text-lg mb-6">
            Continue usando o XBPneus para economizar dinheiro e ajudar o planeta.
          </p>
          <div className="flex gap-4 justify-center">
            <a href="/dashboard/pneus/lista" 
               className="px-6 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-gray-100">
              Gerenciar Pneus
            </a>
            <a href="/dashboard/manutencao/ordens-servico" 
               className="px-6 py-3 bg-white/20 border-2 border-white text-white rounded-lg font-semibold hover:bg-white/30">
              Criar Manutenção
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Economia;
