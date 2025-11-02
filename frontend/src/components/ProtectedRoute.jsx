import { Navigate } from "react-router-dom";
import { getUserRole, isTokenValid } from "../api/auth";
import { hasPermission, getDefaultDashboard } from "../config/permissions";

/**
 * Componente para proteger rotas baseado no role do usuário
 * Redireciona para o dashboard correto se o usuário não tiver permissão
 * Valida se o token é válido antes de permitir acesso
 */
export default function ProtectedRoute({ children, allowedRoles = [] }) {
  const token = localStorage.getItem("access_token");
  const userRole = getUserRole();

  console.log("ProtectedRoute: Token", token ? "Present" : "Absent");
  console.log("ProtectedRoute: Token Valid", isTokenValid());
  console.log("ProtectedRoute: User Role", userRole);

  // Se não estiver autenticado ou o token expirou, redireciona para login
  if (!token || !isTokenValid()) {
    console.warn("ProtectedRoute: Redirecionando para login - token inválido ou ausente");
    return <Navigate to="/login" replace />;
  }

  // Se não tiver role definido, redireciona para login
  if (!userRole) {
    console.warn("ProtectedRoute: Redirecionando para login - role não definido");
    return <Navigate to="/login" replace />;
  }

  // Se a rota tem restrição de roles e o usuário não está na lista
  if (allowedRoles.length > 0 && !allowedRoles.includes(userRole)) {
    // Redireciona para o dashboard correto do usuário
    const dashboard = getDefaultDashboard(userRole);
    console.warn(`ProtectedRoute: Redirecionando para ${dashboard} - usuário não tem permissão`);
    return <Navigate to={dashboard} replace />;
  }

  return children;
}

