/**
 * Configuração centralizada de APIs do sistema XBPneus.
 */

const RAW_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_BASE_URL = RAW_BASE_URL.replace(/\/+$/, '');

const ensureLeadingSlash = (path) => (path.startsWith('/') ? path : `/${path}`);
const ensureTrailingSlash = (path) => (path.endsWith('/') ? path : `${path}/`);

function apiUrl(path) {
  const normalized = ensureTrailingSlash(ensureLeadingSlash(path));
  return `${API_BASE_URL}${normalized}`;
}

function transportadorUrl(path = '') {
  const normalized = `${path}`.replace(/^\/+/, '').replace(/\/+$/, '');
  const base = normalized ? `api/transportador/${normalized}` : 'api/transportador';
  return apiUrl(base);
}

export const API_ENDPOINTS = {
  users: {
    registerFull: apiUrl('api/users/register_full/'),
  },
  auth: {
    login: apiUrl('api/token/'),
    logout: apiUrl('api/auth/logout/'),
    me: apiUrl('api/auth/me/'),
    profile: transportadorUrl('profile/'),
  },
  transportador: {
    frota: {
      veiculos: transportadorUrl('frota/veiculos/'),
      posicoes: transportadorUrl('frota/posicoes/'),
      motoristas: transportadorUrl('frota/motoristas/'),
      implementos: transportadorUrl('frota/implementos/'),
      rastreamento: transportadorUrl('frota/rastreamento/'),
    },
    pneus: {
      pneus: transportadorUrl('pneus/pneus/'),
      aplicacoes: transportadorUrl('pneus/aplicacoes/'),
      eventos: transportadorUrl('pneus/eventos/'),
      manutencao: transportadorUrl('pneus/manutencao/'),
    },
    estoque: {
      produtos: transportadorUrl('estoque/produtos/'),
      movimentacoes: transportadorUrl('estoque/movimentacoes/'),
      categorias: transportadorUrl('estoque/categorias/'),
    },
    manutencao: {
      ordensServico: transportadorUrl('manutencao/ordens-servico/'),
      itensOS: transportadorUrl('manutencao/itens-os/'),
      checklists: transportadorUrl('manutencao/checklists/'),
      planosPreventiva: transportadorUrl('manutencao/planos-preventiva/'),
      historico: transportadorUrl('manutencao/historico/'),
    },
    configuracoes: transportadorUrl('configuracoes/configuracoes/'),
    empresas: transportadorUrl('empresas/empresas/'),
    filiais: transportadorUrl('empresas/filiais/'),
    motoristaInterno: transportadorUrl('motorista-interno/motoristas/'),
    motoristaExterno: transportadorUrl('motorista-externo/motoristas-externos/'),
    vinculosMotorista: transportadorUrl('motorista-interno/vinculos/'),
    jornadasMotorista: transportadorUrl('motorista-interno/jornadas/'),
    mensagensMotorista: transportadorUrl('motorista-interno/mensagens/'),
    alertasMotorista: transportadorUrl('motorista-interno/alertas/'),
    alocacoesMotorista: transportadorUrl('motorista-externo/alocacoes-motorista/'),
    combustivel: {
      postos: transportadorUrl('combustivel/postos/'),
      abastecimentos: transportadorUrl('combustivel/abastecimentos/'),
      consumoMensal: transportadorUrl('combustivel/consumo-mensal/'),
    },
    multas: {
      multas: transportadorUrl('multas/multas/'),
      recursos: transportadorUrl('multas/recursos/'),
      pontuacao: transportadorUrl('multas/pontuacao-cnh/'),
    },
    rastreamento: {
      posicoes: transportadorUrl('rastreamento/posicoes/'),
      cercas: transportadorUrl('rastreamento/cercas/'),
      violacoes: transportadorUrl('rastreamento/violacoes/'),
      historico: transportadorUrl('rastreamento/historico/'),
    },
  },
};

export default API_ENDPOINTS;
