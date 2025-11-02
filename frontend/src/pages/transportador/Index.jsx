import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../../api/http";
import AlertasWidget from "../../components/AlertasWidget";

function Card({ title, value, gradient }) {
  return (
    <div className={`rounded-2xl p-6 text-white shadow-lg ${gradient}`}>
      <div className="text-sm opacity-90 mb-2">{title}</div>
      <div className="text-3xl font-extrabold">{value}</div>
    </div>
  );
}

export default function IndexTransportador(){
  const [m, setM] = useState(null);
  const [err, setErr] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(()=>{
    let mounted = true;
    setLoading(true);
    api.get("/api/transportador/dashboard/")
      .then(r => { 
        if (mounted) {
          setM(r.data);
          setLoading(false);
        }
      })
      .catch(e => { 
        if (mounted) {
          setErr(e);
          setLoading(false);
        }
      });
    return () => { mounted = false; }
  }, []);
  
  // Loading state
  if (loading) {
    return (
      <section>
        <h1 className="text-3xl font-extrabold mb-6 bg-clip-text text-transparent"
            style={{ backgroundImage: "var(--xbp-grad)" }}>
          Painel do Transportador
        </h1>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500"></div>
        </div>
      </section>
    );
  }
  
  const totalVeiculos = m?.frota?.total_veiculos || 0;
  const temDados = totalVeiculos > 0;
  
  return (
    <section>
      <h1 className="text-3xl font-extrabold mb-6 bg-clip-text text-transparent"
          style={{ backgroundImage: "var(--xbp-grad)" }}>
        Painel do Transportador
      </h1>
      
      {/* Mensagem de Boas-Vindas para Novos Usuários */}
      {!temDados && (
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-8 text-white mb-8 shadow-xl">
          <h2 className="text-3xl font-bold mb-4">
            👋 Bem-vindo ao XBPneus!
          </h2>
          <p className="text-lg mb-6 opacity-90">
            Comece cadastrando seu primeiro veículo para começar a economizar e ajudar o planeta! 🌍
          </p>
          <div className="flex gap-4 flex-wrap">
            <Link 
              to="/dashboard/frota/veiculos/create"
              className="px-6 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-gray-100 transition shadow-md"
            >
              ➕ Cadastrar Primeiro Veículo
            </Link>
            <Link 
              to="/dashboard/pneus/create"
              className="px-6 py-3 bg-blue-700 text-white rounded-lg font-semibold hover:bg-blue-800 transition shadow-md"
            >
              🛞 Cadastrar Primeiro Pneu
            </Link>
          </div>
        </div>
      )}
      
      {/* Alertas */}
      <AlertasWidget />
      
      {/* Erro */}
      {err && (
        <div className="bg-red-500/10 border border-red-500 rounded-lg p-4 mb-6">
          <p className="text-red-400">Falha ao carregar métricas. Tente novamente mais tarde.</p>
        </div>
      )}
      
      {/* KPIs */}
      {m && (
        <>
          <h2 className="text-xl font-bold mb-4 text-gray-200">📊 Visão Geral</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <Card 
              title="Total Veículos" 
              value={m.frota.total_veiculos}
              gradient="bg-gradient-to-br from-blue-500 to-blue-600"
            />
            <Card 
              title="Veículos Ativos" 
              value={m.frota.veiculos_ativos}
              gradient="bg-gradient-to-br from-green-500 to-green-600"
            />
            <Card 
              title="Total Posições" 
              value={m.pneus.total_posicoes}
              gradient="bg-gradient-to-br from-purple-500 to-purple-600"
            />
            <Card 
              title="Posições Ocupadas" 
              value={m.pneus.posicoes_ocupadas}
              gradient="bg-gradient-to-br from-indigo-500 to-indigo-600"
            />
          </div>
          
          <h2 className="text-xl font-bold mb-4 text-gray-200">🔧 Manutenção</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <Card 
              title="OS Abertas" 
              value={m.manutencao.os_abertas}
              gradient="bg-gradient-to-br from-yellow-500 to-yellow-600"
            />
            <Card 
              title="OS Em Andamento" 
              value={m.manutencao.os_em_andamento}
              gradient="bg-gradient-to-br from-orange-500 to-orange-600"
            />
            <Card 
              title="Entradas (30d)" 
              value={m.estoque.entradas_30d}
              gradient="bg-gradient-to-br from-teal-500 to-teal-600"
            />
            <Card 
              title="Saídas (30d)" 
              value={m.estoque.saidas_30d}
              gradient="bg-gradient-to-br from-cyan-500 to-cyan-600"
            />
          </div>
        </>
      )}
    </section>
  );
}

