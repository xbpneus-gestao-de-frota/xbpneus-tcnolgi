import axios from "axios";

const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000" });

api.interceptors.request.use((cfg) => {
  // Não adicionar token em requisições de login e registro
  const isAuthEndpoint = cfg.url && (cfg.url.includes('/login/') || cfg.url.includes('/register/'));
  
  if (!isAuthEndpoint) {
    const t = localStorage.getItem("access_token");
    if (t) cfg.headers.Authorization = `Bearer ${t}`;
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
    
    if (!original || original._retry) {
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
        const { data } = await axios.post((import.meta.env.VITE_API_URL || "http://localhost:8000") + "/api/token/refresh/", { refresh });
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

export default api;
