import { useState } from "react";
import { useNavigate, Link, useLocation } from "react-router-dom";
import { login } from "../api/auth";

export default function Login() {
  const [username, setUsername] = useState("");
  const [senha, setSenha] = useState("");
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");
  const nav = useNavigate();
  const loc = useLocation();

  async function onSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setMsg("");
    try {
      const { userRole, redirectUrl } = \1
navigate('/dashboard/transportador');

      console.log("Login successful. User Role:", userRole);
      console.log("Redirecting to Dashboard:", redirectUrl);
      nav(redirectUrl, { replace: true });
    } catch (error) {
      console.error("Login failed:", error);
      if (error.response && error.response.data && error.response.data.detail) {
        setMsg(error.response.data.detail);
      } else if (error.response?.status === 401) {
        // Tratamento específico para 401 (Unauthorized)
        setMsg("E-mail ou senha inválidos. Verifique suas credenciais.");
      } else if (error.response?.status === 403) {
        // Tratamento para 403 (Forbidden) - Pode ser bloqueio (AXES) ou não aprovado
        // O backend deve retornar uma mensagem específica, mas usamos um fallback
        setMsg(error.response.data?.error || "Acesso negado. Sua conta pode estar inativa, não aprovada ou bloqueada por segurança.");
      } else {
        setMsg(error.message || "Falha no login. Verifique sua conexão ou tente novamente.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="bg-gray-100 flex flex-col items-center justify-start min-h-screen pt-8 md:pt-16 relative overflow-x-hidden">
      {/* Mascote lateral esquerda */}
      <img
        src="/static/manutenção.png"
        alt="Mascote manutenção"
        className="hidden lg:block absolute left-2 xl:left-4 top-1/4 object-contain max-w-lg"
        style={{ zIndex: 1 }}
      />

      {/* Mascote lateral direita */}
      <img
        src="/static/frota.png"
        alt="Mascote frota"
        className="hidden lg:block absolute right-2 xl:right-4 top-1/4 object-contain max-w-lg"
        style={{ zIndex: 1 }}
      />

      {/* Logo */}
      <h1
        className="font-black text-center mb-8 md:mb-12 z-10 px-4"
        style={{
          fontSize: "clamp(3rem, 10vw, 7.5rem)",
          fontWeight: 900,
          background: "linear-gradient(135deg, #60a5fa, #6366f1, #7c3aed)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
          backgroundClip: "text",
          textShadow: "4px 4px 12px rgba(0,0,0,0.5)",
          letterSpacing: "0.05em",
          textTransform: "uppercase",
        }}
      >
        XBPNEUS
      </h1>

      {/* Card de Login */}
      <div className="bg-white shadow-2xl rounded-xl p-6 md:p-8 max-w-md w-full mx-4" style={{ zIndex: 20, position: "relative" }}>
        {msg && (
          <div className="mb-4 p-3 rounded bg-red-100 text-red-700">
            {msg}
          </div>
        )}

        <form onSubmit={onSubmit} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              E-mail
            </label>
            <input
              type="text"
              id="email"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 text-blue-900"
            />
          </div>

          <div>
            <label htmlFor="senha" className="block text-sm font-medium text-gray-700 mb-1">
              Senha
            </label>
            <input
              type="password"
              id="senha"
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              required
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 text-blue-900"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 text-white py-2 rounded-lg hover:opacity-90 disabled:opacity-50 font-medium shadow-lg"
          >
            {loading ? "Entrando..." : "Entrar"}
          </button>
        </form>

        <div className="mt-6 text-center space-y-2">
          <Link
            to="/cadastro"
            className="block text-lg font-semibold text-blue-700 hover:text-blue-800 underline"
          >
            Quero me cadastrar
          </Link>
        </div>
      </div>
    </div>
  );
}

