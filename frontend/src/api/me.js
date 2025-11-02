import api from "./http";

export async function getEmpresaId() {
  try {
    const { data } = await api.get("/api/users/me/");
    return data?.empresa || data?.empresa_id || data?.empresa?.id || null;
  } catch {
    return null;
  }
}
