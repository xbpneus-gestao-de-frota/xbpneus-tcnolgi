import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const PUBLIC_ENDPOINTS = new Set([
  "/api/token/",
  "/api/token/refresh/",
  "/api/users/register_full/",
]);

const api = axios.create({ baseURL: BASE_URL });

function isPublicRequest(cfg) {
  if (!cfg?.url) {
    return false;
  }

  const referenceBase = cfg.baseURL || BASE_URL;

  try {
    const resolved = new URL(cfg.url, referenceBase);
    const normalizedPath = resolved.pathname.endsWith("/")
      ? resolved.pathname
      : `${resolved.pathname}/`;
    return PUBLIC_ENDPOINTS.has(normalizedPath);
  } catch (error) {
    console.warn("Não foi possível normalizar URL da requisição:", error);
    return false;
  }
}

api.interceptors.request.use((cfg) => {
  if (!isPublicRequest(cfg)) {
    const token = localStorage.getItem("access_token");
    if (token) {
      cfg.headers.Authorization = `Bearer ${token}`;
    }
  }
  return cfg;
});

let isRefreshing = false;
let queue = [];

function processQueue(error, token = null) {
  queue.forEach(p => token ? p.resolve(token) : p.reject(error));
  queue = [];
}

api.interceptors.response.use(
  (resp) => resp,
  async (error) => {
    const original = error.config;
    
    // Tratamento de 403 (Forbidden - Acesso Negado)
    if (error.response && error.response.status === 403) {
      console.error("HTTP 403 - Acesso Negado:", error.response.data);
      return Promise.reject(error);
    }
    
    if (!original || original._retry || original._skipAuthRefresh) {
      return Promise.reject(error);
    }
    
    // Tratamento de 401 (Unauthorized - Token Inválido ou Expirado)
    if (error.response && error.response.status === 401) {
      console.warn("HTTP 401 - Token inválido ou expirado");
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          queue.push({ resolve, reject });
        }).then((token) => {
          original.headers.Authorization = `Bearer ${token}`;
          return api(original);
        }).catch(Promise.reject);
      }

      original._retry = true;
      isRefreshing = true;
      const refresh = localStorage.getItem("refresh_token");
      if (!refresh) {
        console.error("Refresh token não disponível, redirecionando para login");
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user_role");
        localStorage.removeItem("user_id");
        window.location.href = "/login";
        return Promise.reject(error);
      }
      try {
        console.log("Tentando renovar token...");
        const { data } = await api.post(
          "/api/token/refresh/",
          { refresh },
          { _skipAuthRefresh: true }
        );
        const newAccess = data.access;
        localStorage.setItem("access_token", newAccess);
        api.defaults.headers.common.Authorization = `Bearer ${newAccess}`;
        console.log("Token renovado com sucesso");
        processQueue(null, newAccess);
        return api(original);
      } catch (e) {
        console.error("Erro ao renovar token:", e);
        processQueue(e, null);
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user_role");
        localStorage.removeItem("user_id");
        window.location.href = "/login";
        return Promise.reject(e);
      } finally {
        isRefreshing = false;
      }
    }
    return Promise.reject(error);
  }
);

export const get = (...args) => api.get(...args);
export const post = (...args) => api.post(...args);
export const put = (...args) => api.put(...args);
export const patch = (...args) => api.patch(...args);
export const del = (...args) => api.delete(...args);

export default api;
