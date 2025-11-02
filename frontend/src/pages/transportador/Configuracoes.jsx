import { useState, useEffect } from "react";
import api from "../../api/http";
import PageHeader from "../../components/PageHeader";
import Loader from "../../components/Loader";
import ErrorState from "../../components/ErrorState";

export default function Configuracoes() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [abas, setAbas] = useState("usuarios");
  const [usuarios, setUsuarios] = useState([
    {
      id: 1,
      nome: "João Silva",
      email: "joao@xbpneus.com",
      role: "admin",
      status: "ativo",
      ultimoAcesso: "2025-10-18"
    },
    {
      id: 2,
      nome: "Maria Santos",
      email: "maria@xbpneus.com",
      role: "gerente",
      status: "ativo",
      ultimoAcesso: "2025-10-17"
    },
    {
      id: 3,
      nome: "Pedro Oliveira",
      email: "pedro@xbpneus.com",
      role: "operador",
      status: "ativo",
      ultimoAcesso: "2025-10-16"
    }
  ]);

  const [novoUsuario, setNovoUsuario] = useState({
    nome: "",
    email: "",
    role: "operador"
  });

  const [showFormNovoUsuario, setShowFormNovoUsuario] = useState(false);

  useEffect(() => {
    setLoading(false);
  }, []);

  const adicionarUsuario = (e) => {
    e.preventDefault();
    if (novoUsuario.nome && novoUsuario.email) {
      setUsuarios([...usuarios, {
        id: usuarios.length + 1,
        ...novoUsuario,
        status: "ativo",
        ultimoAcesso: new Date().toISOString().split("T")[0]
      }]);
      setNovoUsuario({ nome: "", email: "", role: "operador" });
      setShowFormNovoUsuario(false);
    }
  };

  const removerUsuario = (id) => {
    setUsuarios(usuarios.filter(u => u.id !== id));
  };

  const atualizarRoleUsuario = (id, novoRole) => {
    setUsuarios(usuarios.map(u =>
      u.id === id ? { ...u, role: novoRole } : u
    ));
  };

  const permissoes = {
    admin: ["Gerenciar usuários", "Configurar sistema", "Acessar relatórios", "Gerenciar frota", "Gerenciar pneus", "Gerenciar estoque", "Gerenciar manutenção"],
    gerente: ["Acessar relatórios", "Gerenciar frota", "Gerenciar pneus", "Gerenciar estoque", "Gerenciar manutenção"],
    operador: ["Acessar relatórios", "Gerenciar frota", "Gerenciar pneus"]
  };

  if (loading) return <Loader />;
  if (error) return <ErrorState message={error} />;

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <PageHeader 
        title="Configurações" 
        subtitle="Gerenciar usuários, permissões e preferências do sistema"
      />

      {/* Abas */}
      <div className="bg-white rounded-xl shadow-md mb-8">
        <div className="flex border-b border-gray-200">
          {["usuarios", "permissoes", "sistema"].map((aba) => (
            <button
              key={aba}
              onClick={() => setAbas(aba)}
              className={`flex-1 py-4 px-6 font-medium transition-colors ${
                abas === aba
                  ? "border-b-2 border-blue-500 text-blue-600"
                  : "text-gray-600 hover:text-gray-800"
              }`}
            >
              {aba === "usuarios" ? "👥 Usuários" :
               aba === "permissoes" ? "🔐 Permissões" :
               "⚙️ Sistema"}
            </button>
          ))}
        </div>
      </div>

      {/* Conteúdo das Abas */}
      {abas === "usuarios" && (
        <div className="space-y-6">
          {/* Botão Adicionar Usuário */}
          <div className="flex justify-end">
            <button
              onClick={() => setShowFormNovoUsuario(!showFormNovoUsuario)}
              className="px-6 py-2 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 transition-colors"
            >
              ➕ Adicionar Usuário
            </button>
          </div>

          {/* Formulário Novo Usuário */}
          {showFormNovoUsuario && (
            <div className="bg-white rounded-xl shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Novo Usuário</h3>
              <form onSubmit={adicionarUsuario} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Nome</label>
                    <input
                      type="text"
                      value={novoUsuario.nome}
                      onChange={(e) => setNovoUsuario({ ...novoUsuario, nome: e.target.value })}
                      className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Nome completo"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">E-mail</label>
                    <input
                      type="email"
                      value={novoUsuario.email}
                      onChange={(e) => setNovoUsuario({ ...novoUsuario, email: e.target.value })}
                      className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="email@exemplo.com"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Função</label>
                  <select
                    value={novoUsuario.role}
                    onChange={(e) => setNovoUsuario({ ...novoUsuario, role: e.target.value })}
                    className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="operador">Operador</option>
                    <option value="gerente">Gerente</option>
                    <option value="admin">Administrador</option>
                  </select>
                </div>
                <div className="flex gap-4">
                  <button
                    type="submit"
                    className="px-6 py-2 bg-green-500 text-white rounded-lg font-medium hover:bg-green-600 transition-colors"
                  >
                    Adicionar
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowFormNovoUsuario(false)}
                    className="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-400 transition-colors"
                  >
                    Cancelar
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Lista de Usuários */}
          <div className="bg-white rounded-xl shadow-md overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Nome</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700">E-mail</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Função</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Status</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Último Acesso</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {usuarios.map((usuario) => (
                    <tr key={usuario.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-3 px-4 text-gray-800 font-medium">{usuario.nome}</td>
                      <td className="py-3 px-4 text-gray-600">{usuario.email}</td>
                      <td className="py-3 px-4">
                        <select
                          value={usuario.role}
                          onChange={(e) => atualizarRoleUsuario(usuario.id, e.target.value)}
                          className="px-3 py-1 rounded-lg border border-gray-300 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                          <option value="operador">Operador</option>
                          <option value="gerente">Gerente</option>
                          <option value="admin">Administrador</option>
                        </select>
                      </td>
                      <td className="py-3 px-4">
                        <span className="px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          {usuario.status === "ativo" ? "Ativo" : "Inativo"}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-gray-600 text-sm">{usuario.ultimoAcesso}</td>
                      <td className="py-3 px-4">
                        <button
                          onClick={() => removerUsuario(usuario.id)}
                          className="text-red-500 hover:text-red-700 font-medium text-sm"
                        >
                          Remover
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {abas === "permissoes" && (
        <div className="space-y-6">
          <h3 className="text-lg font-semibold text-gray-800">Permissões por Função</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {Object.entries(permissoes).map(([role, perms]) => (
              <div key={role} className="bg-white rounded-xl shadow-md p-6">
                <h4 className="text-lg font-semibold text-gray-800 mb-4 capitalize">
                  {role === "admin" ? "👑 Administrador" :
                   role === "gerente" ? "👔 Gerente" :
                   "👤 Operador"}
                </h4>
                <ul className="space-y-2">
                  {perms.map((perm, idx) => (
                    <li key={idx} className="flex items-center gap-2 text-gray-700">
                      <span className="text-green-500">✓</span>
                      {perm}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      )}

      {abas === "sistema" && (
        <div className="space-y-6">
          <div className="bg-white rounded-xl shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Preferências do Sistema</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <label className="text-gray-700 font-medium">Notificações por E-mail</label>
                <input type="checkbox" defaultChecked className="w-5 h-5 rounded" />
              </div>
              <div className="flex items-center justify-between">
                <label className="text-gray-700 font-medium">Notificações Push</label>
                <input type="checkbox" defaultChecked className="w-5 h-5 rounded" />
              </div>
              <div className="flex items-center justify-between">
                <label className="text-gray-700 font-medium">Modo Escuro</label>
                <input type="checkbox" className="w-5 h-5 rounded" />
              </div>
              <div className="flex items-center justify-between">
                <label className="text-gray-700 font-medium">Autenticação de Dois Fatores</label>
                <input type="checkbox" className="w-5 h-5 rounded" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Segurança</h3>
            <div className="space-y-4">
              <button className="w-full px-6 py-2 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 transition-colors">
                🔑 Alterar Senha
              </button>
              <button className="w-full px-6 py-2 bg-orange-500 text-white rounded-lg font-medium hover:bg-orange-600 transition-colors">
                🔐 Ativar Autenticação de Dois Fatores
              </button>
              <button className="w-full px-6 py-2 bg-red-500 text-white rounded-lg font-medium hover:bg-red-600 transition-colors">
                🚪 Desconectar de Todos os Dispositivos
              </button>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Informações do Sistema</h3>
            <div className="space-y-2 text-gray-700">
              <p><strong>Versão:</strong> 1.0.0</p>
              <p><strong>Última Atualização:</strong> 18 de outubro de 2025</p>
              <p><strong>Ambiente:</strong> Produção</p>
              <p><strong>Suporte:</strong> suporte@xbpneus.com</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

