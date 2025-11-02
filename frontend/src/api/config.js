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
      documentos: transportadorUrl('frota/documentos/'),
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
    almoxarifado: {
      almoxarifados: transportadorUrl('almoxarifado/almoxarifados/'),
      locaisEstoque: transportadorUrl('almoxarifado/locais/'),
    },
    cargas: transportadorUrl('cargas/cargas/'),
    pecas: transportadorUrl('pecas/pecas/'),
    ferramentas: transportadorUrl('ferramentas/ferramentas/'),
    epis: transportadorUrl('epis/epis/'),
    treinamentos: transportadorUrl('treinamentos/treinamentos/'),
    compliance: transportadorUrl('compliance/documentos/'),
    alertas: transportadorUrl('alertas/alertas/'),
    integracoes: transportadorUrl('integracoes/integracoes/'),
    configuracoes: transportadorUrl('configuracoes/configuracoes/'),
    relatorios: transportadorUrl('relatorios/relatorios/'),
    notasFiscais: transportadorUrl('notas_fiscais/notas/'),
    auditoria: transportadorUrl('auditoria/logs/'),
    empresas: transportadorUrl('empresas/empresas/'),
    filiais: transportadorUrl('empresas/filiais/'),
    motoristaInterno: transportadorUrl('motorista-interno/motoristas/'),
    motoristaExterno: transportadorUrl('motorista-externo/motoristas-externos/'),
    vinculosMotorista: transportadorUrl('motorista-interno/vinculos/'),
    jornadasMotorista: transportadorUrl('motorista-interno/jornadas/'),
    mensagensMotorista: transportadorUrl('motorista-interno/mensagens/'),
    alertasMotorista: transportadorUrl('motorista-interno/alertas/'),
    alocacoesMotorista: transportadorUrl('motorista-externo/alocacoes-motorista/'),
    clientes: transportadorUrl('clientes/clientes/'),
    contatosClientes: transportadorUrl('clientes/contatos/'),
    fornecedores: transportadorUrl('fornecedores/fornecedores/'),
    contatosFornecedores: transportadorUrl('fornecedores/contatos/'),
    viagens: transportadorUrl('viagens/viagens/'),
    cargasViagem: transportadorUrl('viagens/cargas/'),
    paradasViagem: transportadorUrl('viagens/paradas/'),
    entregas: transportadorUrl('entregas/entregas/'),
    pods: transportadorUrl('entregas/pods/'),
    ocorrenciasEntregas: transportadorUrl('entregas/ocorrencias/'),
    tentativasEntregas: transportadorUrl('entregas/tentativas/'),
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
    contratos: {
      contratos: transportadorUrl('contratos/contratos/'),
      aditivos: transportadorUrl('contratos/aditivos/'),
    },
    custos: {
      categorias: transportadorUrl('custos/categorias/'),
      custos: transportadorUrl('custos/custos/'),
      custoPorKm: transportadorUrl('custos/custo-por-km/'),
    },
    pagamentos: {
      contasPagar: transportadorUrl('pagamentos/contas-pagar/'),
      contasReceber: transportadorUrl('pagamentos/contas-receber/'),
      pagamentos: transportadorUrl('pagamentos/pagamentos/'),
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
