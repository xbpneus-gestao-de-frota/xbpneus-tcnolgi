import { useState, useEffect } from "react";
import api from "../../api/http";
import PageHeader from "../../components/PageHeader";
import Loader from "../../components/Loader";
import ErrorState from "../../components/ErrorState";

export default function Financeiro() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [financeiro, setFinanceiro] = useState({
    despesas_mes: 0,
    cpk: 0,
    receita_mes: 0,
    lucro_mes: 0,
    transacoes: []
  });
  const [filtro, setFiltro] = useState("mes");

  useEffect(() => {
    loadFinanceiro();
  }, [filtro]);

  const loadFinanceiro = async () => {
    try {
      setLoading(true);
      // Simulando dados - em produção seria um endpoint real
      const mockData = {
        despesas_mes: 12500.50,
        cpk: 2.35,
        receita_mes: 45000.00,
        lucro_mes: 32499.50,
        transacoes: [
          { id: 1, descricao: "Combustível", valor: -2500, data: "2025-10-18", tipo: "despesa" },
          { id: 2, descricao: "Manutenção Veículo", valor: -1200, data: "2025-10-17", tipo: "despesa" },
          { id: 3, descricao: "Compra de Pneus", valor: -3500, data: "2025-10-16", tipo: "despesa" },
          { id: 4, descricao: "Frete Realizado", valor: 5000, data: "2025-10-15", tipo: "receita" },
          { id: 5, descricao: "Manutenção Preventiva", valor: -1800, data: "2025-10-14", tipo: "despesa" },
          { id: 6, descricao: "Frete Realizado", valor: 4500, data: "2025-10-13", tipo: "receita" },
        ]
      };
      setFinanceiro(mockData);
    } catch (ex) {
      console.error("Erro ao carregar dados financeiros:", ex);
      setError("Falha ao carregar dados financeiros. Tente novamente mais tarde.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loader />;
  if (error) return <ErrorState message={error} />;

  const formatCurrency = (value) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL"
    }).format(value);
  };

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <PageHeader 
        title="Financeiro" 
        subtitle="Controle de despesas, receitas e CPK (Custo Por Quilômetro)"
      />

      {/* Cards de Resumo */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-md p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-600">Receita do Mês</span>
            <span className="text-2xl">💰</span>
          </div>
          <div className="text-2xl font-bold text-green-600">{formatCurrency(financeiro.receita_mes)}</div>
          <p className="text-xs text-gray-500 mt-2">+5% vs mês anterior</p>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-600">Despesas do Mês</span>
            <span className="text-2xl">💸</span>
          </div>
          <div className="text-2xl font-bold text-red-600">{formatCurrency(financeiro.despesas_mes)}</div>
          <p className="text-xs text-gray-500 mt-2">-3% vs mês anterior</p>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-600">Lucro do Mês</span>
            <span className="text-2xl">📈</span>
          </div>
          <div className="text-2xl font-bold text-blue-600">{formatCurrency(financeiro.lucro_mes)}</div>
          <p className="text-xs text-gray-500 mt-2">+8% vs mês anterior</p>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-600">CPK (R$/km)</span>
            <span className="text-2xl">📊</span>
          </div>
          <div className="text-2xl font-bold text-purple-600">R$ {financeiro.cpk.toFixed(2)}</div>
          <p className="text-xs text-gray-500 mt-2">Custo por quilômetro</p>
        </div>
      </div>

      {/* Filtros */}
      <div className="bg-white rounded-xl shadow-md p-6 mb-8">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Período</h2>
        <div className="flex gap-4 flex-wrap">
          {["dia", "semana", "mes", "trimestre", "ano"].map((periodo) => (
            <button
              key={periodo}
              onClick={() => setFiltro(periodo)}
              className={`px-6 py-2 rounded-lg font-medium transition-colors ${
                filtro === periodo
                  ? "bg-blue-500 text-white"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              {periodo.charAt(0).toUpperCase() + periodo.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Transações */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Transações Recentes</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="border-b border-gray-200">
              <tr>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Descrição</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Data</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Tipo</th>
                <th className="text-right py-3 px-4 font-semibold text-gray-700">Valor</th>
              </tr>
            </thead>
            <tbody>
              {financeiro.transacoes.map((transacao) => (
                <tr key={transacao.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4 text-gray-800">{transacao.descricao}</td>
                  <td className="py-3 px-4 text-gray-600">{new Date(transacao.data).toLocaleDateString("pt-BR")}</td>
                  <td className="py-3 px-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      transacao.tipo === "receita"
                        ? "bg-green-100 text-green-800"
                        : "bg-red-100 text-red-800"
                    }`}>
                      {transacao.tipo === "receita" ? "Receita" : "Despesa"}
                    </span>
                  </td>
                  <td className={`py-3 px-4 text-right font-semibold ${
                    transacao.valor > 0 ? "text-green-600" : "text-red-600"
                  }`}>
                    {formatCurrency(transacao.valor)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Ações */}
      <div className="mt-8 bg-white rounded-xl shadow-md p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Ações</h2>
        <div className="flex gap-4 flex-wrap">
          <button className="px-6 py-2 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 transition-colors">
            💳 Adicionar Transação
          </button>
          <button className="px-6 py-2 bg-green-500 text-white rounded-lg font-medium hover:bg-green-600 transition-colors">
            📊 Gerar Relatório Financeiro
          </button>
          <button className="px-6 py-2 bg-purple-500 text-white rounded-lg font-medium hover:bg-purple-600 transition-colors">
            📥 Importar Extrato Bancário
          </button>
        </div>
      </div>
    </div>
  );
}

