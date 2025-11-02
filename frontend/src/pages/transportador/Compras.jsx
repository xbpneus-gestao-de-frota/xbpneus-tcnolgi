import { useState, useEffect } from "react";
import api from "../../api/http";
import PageHeader from "../../components/PageHeader";
import Loader from "../../components/Loader";
import ErrorState from "../../components/ErrorState";

export default function Compras() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filtro, setFiltro] = useState("todos");
  const [carrinho, setCarrinho] = useState([]);
  const [showCarrinho, setShowCarrinho] = useState(false);

  const [produtos, setProdutos] = useState([
    {
      id: 1,
      nome: "Pneu Michelin XZE 295/80R22.5",
      preco: 850.00,
      categoria: "pneus",
      estoque: 15,
      desconto: 5,
      imagem: "🛞",
      descricao: "Pneu de carga de alta performance"
    },
    {
      id: 2,
      nome: "Pneu Bridgestone R-Drive 295/80R22.5",
      preco: 920.00,
      categoria: "pneus",
      estoque: 8,
      desconto: 0,
      imagem: "🛞",
      descricao: "Pneu resistente para longas distâncias"
    },
    {
      id: 3,
      nome: "Pneu Continental HDC1 295/80R22.5",
      preco: 780.00,
      categoria: "pneus",
      estoque: 20,
      desconto: 10,
      imagem: "🛞",
      descricao: "Pneu econômico com boa durabilidade"
    },
    {
      id: 4,
      nome: "Kit Manutenção Preventiva",
      preco: 450.00,
      categoria: "manutencao",
      estoque: 12,
      desconto: 0,
      imagem: "🔧",
      descricao: "Filtros, óleo e fluidos essenciais"
    },
    {
      id: 5,
      nome: "Jogo de Pastilhas de Freio",
      preco: 320.00,
      categoria: "pecas",
      estoque: 25,
      desconto: 8,
      imagem: "⚙️",
      descricao: "Pastilhas de freio de qualidade premium"
    },
    {
      id: 6,
      nome: "Bateria Automotiva 12V 150Ah",
      preco: 680.00,
      categoria: "pecas",
      estoque: 10,
      desconto: 0,
      imagem: "🔋",
      descricao: "Bateria de alta capacidade"
    },
    {
      id: 7,
      nome: "Óleo Lubrificante 15W40 (20L)",
      preco: 280.00,
      categoria: "manutencao",
      estoque: 30,
      desconto: 5,
      imagem: "🛢️",
      descricao: "Óleo mineral para motores diesel"
    },
    {
      id: 8,
      nome: "Correia de Distribuição",
      preco: 450.00,
      categoria: "pecas",
      estoque: 5,
      desconto: 0,
      imagem: "⚙️",
      descricao: "Correia de distribuição de qualidade"
    }
  ]);

  useEffect(() => {
    setLoading(false);
  }, []);

  const adicionarAoCarrinho = (produto) => {
    const itemExistente = carrinho.find(item => item.id === produto.id);
    if (itemExistente) {
      setCarrinho(carrinho.map(item =>
        item.id === produto.id
          ? { ...item, quantidade: item.quantidade + 1 }
          : item
      ));
    } else {
      setCarrinho([...carrinho, { ...produto, quantidade: 1 }]);
    }
  };

  const removerDoCarrinho = (produtoId) => {
    setCarrinho(carrinho.filter(item => item.id !== produtoId));
  };

  const atualizarQuantidade = (produtoId, novaQuantidade) => {
    if (novaQuantidade <= 0) {
      removerDoCarrinho(produtoId);
    } else {
      setCarrinho(carrinho.map(item =>
        item.id === produtoId
          ? { ...item, quantidade: novaQuantidade }
          : item
      ));
    }
  };

  const produtosFiltrados = filtro === "todos"
    ? produtos
    : produtos.filter(p => p.categoria === filtro);

  const totalCarrinho = carrinho.reduce((total, item) => {
    const precoComDesconto = item.preco * (1 - item.desconto / 100);
    return total + (precoComDesconto * item.quantidade);
  }, 0);

  const formatCurrency = (value) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL"
    }).format(value);
  };

  if (loading) return <Loader />;
  if (error) return <ErrorState message={error} />;

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <PageHeader 
        title="Compras" 
        subtitle="Loja interna com catálogo de pneus, peças e insumos"
      />

      {/* Botão Carrinho Flutuante */}
      {carrinho.length > 0 && (
        <button
          onClick={() => setShowCarrinho(!showCarrinho)}
          className="fixed bottom-8 right-8 bg-blue-500 text-white rounded-full p-4 shadow-lg hover:bg-blue-600 transition-colors flex items-center gap-2 z-50"
        >
          <span className="text-2xl">🛒</span>
          <span className="font-bold">{carrinho.length}</span>
        </button>
      )}

      {/* Painel do Carrinho */}
      {showCarrinho && (
        <div className="fixed bottom-24 right-8 bg-white rounded-xl shadow-xl p-6 w-96 max-h-96 overflow-y-auto z-50">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Carrinho de Compras</h3>
          {carrinho.length === 0 ? (
            <p className="text-gray-600">Carrinho vazio</p>
          ) : (
            <>
              {carrinho.map(item => (
                <div key={item.id} className="border-b border-gray-200 py-3 last:border-b-0">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <p className="font-medium text-gray-800">{item.nome}</p>
                      <p className="text-sm text-gray-600">{formatCurrency(item.preco)}</p>
                    </div>
                    <button
                      onClick={() => removerDoCarrinho(item.id)}
                      className="text-red-500 hover:text-red-700 text-sm"
                    >
                      ✕
                    </button>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => atualizarQuantidade(item.id, item.quantidade - 1)}
                      className="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300"
                    >
                      -
                    </button>
                    <span className="px-3">{item.quantidade}</span>
                    <button
                      onClick={() => atualizarQuantidade(item.id, item.quantidade + 1)}
                      className="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300"
                    >
                      +
                    </button>
                  </div>
                </div>
              ))}
              <div className="border-t border-gray-200 mt-4 pt-4">
                <div className="flex justify-between items-center mb-4">
                  <span className="font-semibold text-gray-800">Total:</span>
                  <span className="text-2xl font-bold text-blue-600">{formatCurrency(totalCarrinho)}</span>
                </div>
                <button className="w-full px-6 py-2 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 transition-colors">
                  Finalizar Compra
                </button>
              </div>
            </>
          )}
        </div>
      )}

      {/* Filtros */}
      <div className="bg-white rounded-xl shadow-md p-6 mb-8">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Categorias</h2>
        <div className="flex gap-4 flex-wrap">
          {["todos", "pneus", "manutencao", "pecas"].map((categoria) => (
            <button
              key={categoria}
              onClick={() => setFiltro(categoria)}
              className={`px-6 py-2 rounded-lg font-medium transition-colors ${
                filtro === categoria
                  ? "bg-blue-500 text-white"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              {categoria === "todos" ? "Todos" : categoria.charAt(0).toUpperCase() + categoria.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Grid de Produtos */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {produtosFiltrados.map((produto) => {
          const precoComDesconto = produto.preco * (1 - produto.desconto / 100);
          return (
            <div key={produto.id} className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow">
              <div className="bg-gradient-to-br from-blue-400 to-purple-500 p-8 flex items-center justify-center h-32">
                <span className="text-6xl">{produto.imagem}</span>
              </div>
              
              <div className="p-4">
                <h3 className="font-semibold text-gray-800 mb-2 line-clamp-2">{produto.nome}</h3>
                <p className="text-sm text-gray-600 mb-4">{produto.descricao}</p>
                
                <div className="flex items-center justify-between mb-4">
                  <div>
                    {produto.desconto > 0 && (
                      <p className="text-xs text-gray-500 line-through">{formatCurrency(produto.preco)}</p>
                    )}
                    <p className="text-lg font-bold text-blue-600">{formatCurrency(precoComDesconto)}</p>
                    {produto.desconto > 0 && (
                      <p className="text-xs text-green-600 font-semibold">-{produto.desconto}%</p>
                    )}
                  </div>
                  <span className={`text-xs font-medium px-2 py-1 rounded ${
                    produto.estoque > 0
                      ? "bg-green-100 text-green-800"
                      : "bg-red-100 text-red-800"
                  }`}>
                    {produto.estoque > 0 ? `${produto.estoque} em estoque` : "Fora de estoque"}
                  </span>
                </div>
                
                <button
                  onClick={() => adicionarAoCarrinho(produto)}
                  disabled={produto.estoque === 0}
                  className={`w-full py-2 rounded-lg font-medium transition-colors ${
                    produto.estoque > 0
                      ? "bg-blue-500 text-white hover:bg-blue-600"
                      : "bg-gray-300 text-gray-600 cursor-not-allowed"
                  }`}
                >
                  {produto.estoque > 0 ? "Adicionar ao Carrinho" : "Indisponível"}
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Seção de Informações */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">📦 Entrega Rápida</h3>
          <p className="text-gray-600">Receba seus pedidos em até 48 horas</p>
        </div>
        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">💳 Parcelamento</h3>
          <p className="text-gray-600">Parcelamos em até 12x sem juros</p>
        </div>
        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">✅ Garantia</h3>
          <p className="text-gray-600">Todos os produtos com garantia de qualidade</p>
        </div>
      </div>
    </div>
  );
}

