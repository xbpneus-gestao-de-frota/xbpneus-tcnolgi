
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Cadastro() {
  const [form, setForm] = useState({
    nome_razao_social: "",
    cnpj: "",
    telefone: "",
    email: "",
    password: "",
    password_confirm: "",
    tipo_cliente: "",
  });
  const [errors, setErrors] = useState({});
  const [showSenha, setShowSenha] = useState(false);
  const [showConfirmar, setShowConfirmar] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const nav = useNavigate();

  const validarCNPJ = (cnpj) => {
    const cleaned = cnpj.replace(/[^\d]/g, "");
    return cleaned.length === 14;
  };

  const handleCNPJChange = (e) => {
    const value = e.target.value.replace(/[^\d]/g, "");
    setForm({ ...form, cnpj: value });
    if (value.length > 0 && !validarCNPJ(value)) {
      setErrors({ ...errors, cnpj: "CNPJ deve ter 14 dígitos" });
    } else {
      const newErrors = { ...errors };
      delete newErrors.cnpj;
      setErrors(newErrors);
    }
  };

  const handleConfirmarSenhaChange = (e) => {
    const value = e.target.value;
    setForm({ ...form, password_confirm: value });
    if (value && form.password !== value) {
      setErrors((prevErrors) => ({ ...prevErrors, password_confirm: "Senhas não coincidem" }));
    } else {
      setErrors((prevErrors) => {
        const newErrors = { ...prevErrors };
        delete newErrors.password_confirm;
        return newErrors;
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});
    setMessage("");

    let hasError = false;
    const newErrors = {};

    if (!form.nome_razao_social) {
      newErrors.nome_razao_social = "Nome/Razão Social é obrigatório";
      hasError = true;
    }

    if (!validarCNPJ(form.cnpj)) {
      newErrors.cnpj = "CNPJ inválido";
      hasError = true;
    }

    if (!form.email) {
      newErrors.email = "Email é obrigatório";
      hasError = true;
    }

    if (!form.password || form.password.length < 6) {
      newErrors.password = "Senha deve ter no mínimo 6 caracteres";
      hasError = true;
    }

    if (form.password !== form.password_confirm) {
      newErrors.password_confirm = "Senhas não coincidem";
      hasError = true;
    }

    if (!form.tipo_cliente) {
      newErrors.tipo_cliente = "Tipo de usuário é obrigatório";
      hasError = true;
    }

    if (hasError) {
      setErrors(newErrors);
      return;
    }

    setLoading(true);

    try {
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      
      // Usar o endpoint de registro full para todos os tipos de usuário (Backend faz o roteamento)
      const endpoint = '/api/users/register_full/';
      
      // Preparar payload
      const payload = {
        email: form.email,
        password: form.password,
        password_confirm: form.password_confirm,
        telefone: form.telefone,
        nome_razao_social: form.nome_razao_social,
        cnpj: form.cnpj,
        tipo_usuario: form.tipo_cliente, // Adicionado o tipo de usuário ao payload
      };

      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.ok) {
        setLoading(false);
        // Redirecionar para página pós-cadastro
        nav("/pos-cadastro");
      } else {
        setLoading(false);
        
        // Melhor tratamento de erros - exibir mensagens específicas
        if (data.email) {
          setMessage(`Email: ${Array.isArray(data.email) ? data.email.join(', ') : data.email}`);
        } else if (data.cnpj) {
          setMessage(`CNPJ: ${Array.isArray(data.cnpj) ? data.cnpj.join(', ') : data.cnpj}`);
        } else if (data.password) {
          setMessage(`Senha: ${Array.isArray(data.password) ? data.password.join(', ') : data.password}`);
        } else if (data.detail) {
          setMessage(data.detail);
        } else if (data.non_field_errors) {
          setMessage(Array.isArray(data.non_field_errors) ? data.non_field_errors.join(', ') : data.non_field_errors);
        } else {
          setMessage('Erro ao realizar cadastro. Verifique os dados e tente novamente.');
        }
      }
    } catch (error) {
      setLoading(false);
      setMessage('Erro ao conectar com o servidor. Verifique sua conexão e tente novamente.');
      console.error('Erro no cadastro:', error);
    }
  };

  return (
    <div className="bg-gray-100 flex flex-col items-center justify-center min-h-screen py-8 px-4">
      {/* Logo no topo centralizado */}
      <h1
        className="font-black text-center mb-6 md:mb-8"
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

      <div className="flex items-center justify-center w-full max-w-6xl gap-8">
        {/* Mascote */}
        <div className="hidden lg:flex flex-col items-center justify-center w-1/2">
          <img
            src="/static/configurações.png"
            alt="Mascote XBPNEUS"
            className="w-full max-w-lg"
          />
        </div>

        {/* Painel de Cadastro */}
        <div className="bg-white shadow-2xl rounded-xl p-6 md:p-8 max-w-md w-full lg:w-1/2" style={{ zIndex: 20, position: "relative" }}>
          <h2
            className="text-2xl font-bold text-center mb-6"
            style={{
              background: "linear-gradient(135deg, #60a5fa, #6366f1, #7c3aed)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              backgroundClip: "text",
            }}
          >
            Cadastro
          </h2>

          {message && (
            <div className={`mb-4 p-3 rounded ${
              message.includes('Erro') || message.includes('Email:') || message.includes('CNPJ:') || message.includes('Senha:')
                ? 'bg-red-100 text-red-700 border border-red-300'
                : 'bg-green-100 text-green-700 border border-green-300'
            }`}>
              {message}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <input
                type="text"
                name="nome"
                placeholder="Nome/Razão Social"
                value={form.nome_razao_social}
                onChange={(e) => setForm({ ...form, nome_razao_social: e.target.value })}
                className="w-full border border-gray-300 focus:ring-blue-500 focus:border-blue-500 rounded-lg px-3 py-2 bg-white text-blue-900"
                required
              />
              {errors.nome_razao_social && (
                <div className="text-red-500 text-sm mt-1">{errors.nome_razao_social}</div>
              )}
            </div>

            <div>
              <input
                type="text"
                name="cnpj"
                placeholder="CNPJ (apenas números)"
                value={form.cnpj}
                onChange={handleCNPJChange}
                className="w-full border border-gray-300 focus:ring-blue-500 focus:border-blue-500 rounded-lg px-3 py-2 bg-white text-blue-900"
                maxLength="14"
                required
              />
              {errors.cnpj && (
                <div className="text-red-500 text-sm mt-1">{errors.cnpj}</div>
              )}
            </div>

            <div>
              <input
                type="text"
                name="telefone"
                placeholder="Contato Telefônico"
                value={form.telefone}
                onChange={(e) => setForm({ ...form, telefone: e.target.value })}
                className="w-full border border-gray-300 focus:ring-blue-500 focus:border-blue-500 rounded-lg px-3 py-2 bg-white text-blue-900"
              />
              {errors.contato && (
                <div className="text-red-500 text-sm mt-1">{errors.contato}</div>
              )}
            </div>

            <div>
              <input
                type="email"
                name="email"
                placeholder="E-mail"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                className="w-full border border-gray-300 focus:ring-blue-500 focus:border-blue-500 rounded-lg px-3 py-2 bg-white text-blue-900"
                required
              />
              {errors.email && (
                <div className="text-red-500 text-sm mt-1">{errors.email}</div>
              )}
            </div>

            <div className="relative">
              <input
                type={showSenha ? "text" : "password"}
                name="password"
                placeholder="Senha (mín. 6 caracteres)"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                className="w-full border border-gray-300 focus:ring-blue-500 focus:border-blue-500 rounded-lg px-3 py-2 pr-10 bg-white text-blue-900"
                minLength="6"
                required
              />
              <span
                className="absolute right-3 top-2 text-gray-600 cursor-pointer"
                onClick={() => setShowSenha(!showSenha)}
              >
                👁
              </span>
              {errors.password && (
                <div className="text-red-500 text-sm mt-1">{errors.password}</div>
              )}
            </div>

            <div className="relative">
              <input
                type={showConfirmar ? "text" : "password"}
                name="confirmar_senha"
                placeholder="Confirmar Senha"
                value={form.password_confirm}
                onChange={handleConfirmarSenhaChange}
                className="w-full border border-gray-300 focus:ring-blue-500 focus:border-blue-500 rounded-lg px-3 py-2 pr-10 bg-white text-blue-900"
                required
              />
              <span
                className="absolute right-3 top-2 text-gray-600 cursor-pointer"
                onClick={() => setShowConfirmar(!showConfirmar)}
              >
                👁
              </span>
              {errors.password_confirm && (
                <div className="text-red-500 text-sm mt-1">{errors.password_confirm}</div>
              )}
            </div>

            <div>
              <select
                name="tipo_cliente"
                value={form.tipo_cliente}
                onChange={(e) =>
                  setForm({ ...form, tipo_cliente: e.target.value })
                }
                className="w-full border border-gray-300 focus:ring-blue-500 focus:border-blue-500 rounded-lg px-3 py-2 bg-white text-gray-900"
                style={{ 
                  backgroundColor: "white",
                  opacity: 1,
                  color: form.tipo_cliente ? "#1e40af" : "#6b7280",
                }}
                required
              >
                <option value="" style={{ backgroundColor: "white" }}>Selecione o tipo de usuário</option>
                <option value="transportador" style={{ backgroundColor: "white" }}>Transportador</option>
                <option value="motorista" style={{ backgroundColor: "white" }}>Motorista</option>
                <option value="revenda" style={{ backgroundColor: "white" }}>Revenda</option>
                <option value="borracharia" style={{ backgroundColor: "white" }}>Borracharia</option>
                <option value="recapagem" style={{ backgroundColor: "white" }}>Recapagem</option>
              </select>
              {errors.tipo_cliente && (
                <div className="text-red-500 text-sm mt-1">{errors.tipo_cliente}</div>
              )}
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2 rounded-lg font-medium text-white shadow-lg disabled:opacity-50 hover:opacity-90 transition-opacity"
              style={{
                backgroundImage:
                  "linear-gradient(135deg, #60a5fa, #6366f1, #7c3aed)",
                boxShadow: "3px 3px 8px rgba(0,0,0,0.4)",
              }}
            >
              {loading ? "Processando..." : "Registrar"}
            </button>
          </form>

          <div className="mt-4 text-center">
            <Link
              to="/login"
              className="text-blue-700 hover:text-blue-800 hover:underline"
            >
              Já tem conta? Faça login
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

