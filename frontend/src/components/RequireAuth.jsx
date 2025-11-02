import { Navigate, useLocation } from "react-router-dom";
import { isTokenValid } from "../api/auth";

/**
 * Componente para exigir autenticação
 * Valida se o token é válido antes de permitir acesso
 */
export default function RequireAuth({ children }){
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  const loc = useLocation();
  
  // Verificar se o token existe e é válido
  if (!token || !isTokenValid()) {
    console.warn("RequireAuth: Token inválido ou ausente, redirecionando para login");
    return <Navigate to="/login" state={{ from: loc }} replace />;
  }
  
  return children;
}

