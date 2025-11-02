import api from "./http";
import API_ENDPOINTS from "./config";
import { jwtDecode } from "jwt-decode";

const ROLE_MAP = {
  transportador: "transportador",
  usuariotransportador: "transportador",
  "transportador.usuariotransportador": "transportador",
  motorista: "motorista",
  usuariomotorista: "motorista",
  "motorista.usuariomotorista": "motorista",
  borracharia: "borracharia",
  usuarioborracharia: "borracharia",
  "borracharia.usuarioborracharia": "borracharia",
  revenda: "revenda",
  usuariorevenda: "revenda",
  "revenda.usuariorevenda": "revenda",
  recapagem: "recapagem",
  usuariorecapagem: "recapagem",
  "recapagem.usuariorecapagem": "recapagem",
  motorista_externo: "motorista_externo",
  motoristaexterno: "motorista_externo",
  "motorista.motoristaexterno": "motorista_externo",
};

const DASHBOARD_MAP = {
  transportador: "/transportador/dashboard",
  motorista: "/motorista/dashboard",
  borracharia: "/borracharia/dashboard",
  revenda: "/revenda/dashboard",
  recapagem: "/recapagem/dashboard",
  motorista_externo: "/motorista/dashboard",
};

function sanitizeRole(rawRole) {
  return rawRole
    .trim()
    .toLowerCase()
    .replace(/\s+/g, "")
    .replace(/[\\/]+/g, ".");
}

function normalizeUserRole(rawRole, fallback) {
  if (!rawRole || typeof rawRole !== "string") {
    return fallback;
  }

  const candidate = sanitizeRole(rawRole);

  if (ROLE_MAP[candidate]) {
    return ROLE_MAP[candidate];
  }

  const segments = candidate.split(/[.:]+/).filter(Boolean);
  for (let i = segments.length - 1; i >= 0; i -= 1) {
    const segment = segments[i];
    if (ROLE_MAP[segment]) {
      return ROLE_MAP[segment];
    }
    const withoutUsuario = segment.replace(/^usuario[_-]?/, "");
    if (ROLE_MAP[withoutUsuario]) {
      return ROLE_MAP[withoutUsuario];
    }
  }

  if (candidate.startsWith("usuario")) {
    const trimmed = candidate.replace(/^usuario[_-]?/, "");
    if (ROLE_MAP[trimmed]) {
      return ROLE_MAP[trimmed];
    }
  }

  return fallback;
}

function persistSession(accessToken, refreshToken, userRoleFallback = "transportador") {
  if (!accessToken || !refreshToken) {
    throw new Error("Tokens de autenticação não recebidos.");
  }

  localStorage.setItem("access_token", accessToken);
  localStorage.setItem("refresh_token", refreshToken);

  let decodedToken = null;
  try {
    decodedToken = jwtDecode(accessToken);
  } catch (decodeError) {
    console.error("Falha ao decodificar token JWT:", decodeError);
    throw new Error("Token de acesso inválido recebido do servidor.");
  }

  // O token JWT DEVE conter o user_type. Se não contiver, o backend está errado.
  // userRoleFallback é 'transportador' por padrão.
  const rawRole = decodedToken.user_role || decodedToken.user_type || userRoleFallback;
  const userRole = normalizeUserRole(rawRole, userRoleFallback);
  const userId = decodedToken.user_id;

  if (!userId) {
    throw new Error("Token de acesso não contém o identificador do usuário.");
  }

  localStorage.setItem("user_role", userRole);
  localStorage.setItem("user_id", userId);

  const redirectUrl = DASHBOARD_MAP[userRole] || DASHBOARD_MAP.transportador;

  localStorage.setItem("redirect_url", redirectUrl);

  return { userRole, redirectUrl };
}

function wrapAndThrow(error) {
  if (error.response) {
    const message = error.response.data?.error || error.response.data?.detail;
    if (message) {
      const wrappedError = new Error(message);
      wrappedError.response = error.response;
      throw wrappedError;
    }
  }
  throw error;
}

export async function login(email, password) {
  const timestamp = Date.now();

  try {
    const loginUrl = new URL(API_ENDPOINTS.auth.login);
    loginUrl.searchParams.set("t", timestamp.toString());
    const { data } = await api.post(loginUrl.toString(), { email, password });
    return persistSession(
      data.access,
      data.refresh,
      data.user_role || data.user_type || "transportador",
    );
  } catch (primaryError) {
    const status = primaryError.response?.status;



    console.error("Erro no login principal:", primaryError);
    wrapAndThrow(primaryError);
  }
}

export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user_role");
  localStorage.removeItem("user_id");
  localStorage.removeItem("user_data");
  localStorage.removeItem("redirect_url");
}

export function getAccessToken() {
  return localStorage.getItem("access_token");
}

export function getRefreshToken() {
  return localStorage.getItem("refresh_token");
}

export function getUserRole() {
  return localStorage.getItem("user_role");
}

export function getUserId() {
  return localStorage.getItem("user_id");
}

export function getUserData() {
  const data = localStorage.getItem("user_data");
  return data ? JSON.parse(data) : null;
}

/**
 * Valida se o token JWT é válido e não expirou
 */
export function isTokenValid() {
  const token = localStorage.getItem("access_token");
  if (!token) return false;
  
  try {
    const decoded = jwtDecode(token);
    const currentTime = Date.now() / 1000;
    const isValid = decoded.exp > currentTime;
    
    if (!isValid) {
      console.warn("Token expirado ou inválido");
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("user_role");
      localStorage.removeItem("user_id");
    }
    
    return isValid;
  } catch (e) {
    console.error("Erro ao validar token:", e);
    return false;
  }
}

/**
 * Renova o token de acesso usando o refresh token
 */
export async function refreshToken() {
  try {
    const refresh = localStorage.getItem("refresh_token");
    if (!refresh) {
      throw new Error("Refresh token não disponível");
    }
    
    const { data } = await api.post("/api/token/refresh/", { refresh }, { _skipAuthRefresh: true });
    if (data.access) {
      localStorage.setItem("access_token", data.access);
      console.log("Token renovado com sucesso");
      return true;
    }
  } catch (e) {
    console.error("Erro ao renovar token:", e);
    logout();
    return false;
  }
}

