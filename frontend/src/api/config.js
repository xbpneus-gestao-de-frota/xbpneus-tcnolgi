/**
 * Configuração centralizada de APIs
 * Sistema XBPneus
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  // Autenticação
  users: {
    registerFull: `${API_BASE_URL}/api/users/register_full/`,
  },
  auth: {
    // Login específico do transportador
    login: `${API_BASE_URL}/api/transportador/login/`,
    // Endpoints unificados de autenticação
    logout: `${API_BASE_URL}/api/auth/logout/`,
    me: `${API_BASE_URL}/api/auth/me/`,
    // Endpoints específicos do transportador
    
    profile: `${API_BASE_URL}/api/transportador/profile/`,
  },
  
  // Transportador
  transportador: {
    // Frota
    veiculos: `${API_BASE_URL}/api/transportador/frota/veiculos/`,
    posicoes: `${API_BASE_URL}/api/transportador/frota/posicoes/`,
    
    // Pneus
    pneus: `${API_BASE_URL}/api/transportador/pneus/pneus/`,
    aplicacoes: `${API_BASE_URL}/api/transportador/pneus/aplicacoes/`,
    eventos: `${API_BASE_URL}/api/transportador/pneus/eventos/`,
    
    // Estoque
    estoque: `${API_BASE_URL}/api/transportador/estoque/produtos/`,
    movimentacoes: `${API_BASE_URL}/api/transportador/estoque/movimentacoes/`,
    categorias: `${API_BASE_URL}/api/transportador/estoque/categorias/`,
    
    // Manutenção
    ordensServico: `${API_BASE_URL}/api/transportador/manutencao/ordens-servico/`,
    itensOS: `${API_BASE_URL}/api/transportador/manutencao/itens-os/`,
    checklists: `${API_BASE_URL}/api/transportador/manutencao/checklists/`,
    planosPreventiva: `${API_BASE_URL}/api/transportador/manutencao/planos-preventiva/`,
    historicoManutencao: `${API_BASE_URL}/api/transportador/manutencao/historico/`,
    
    // Almoxarifado
    almoxarifados: `${API_BASE_URL}/api/transportador/almoxarifado/almoxarifados/`,
    locaisEstoque: `${API_BASE_URL}/api/transportador/almoxarifado/locais/`,
    
    // Cargas
    cargas: `${API_BASE_URL}/api/transportador/cargas/cargas/`,
    
    // Peças
    pecas: `${API_BASE_URL}/api/transportador/pecas/pecas/`,
    
    // Ferramentas
    ferramentas: `${API_BASE_URL}/api/transportador/ferramentas/ferramentas/`,
    
    // EPIs
    epis: `${API_BASE_URL}/api/transportador/epis/epis/`,
    
    // Treinamentos
    treinamentos: `${API_BASE_URL}/api/transportador/treinamentos/treinamentos/`,
    
    // Compliance
    compliance: `${API_BASE_URL}/api/transportador/compliance/documentos/`,
    
    // Alertas
    alertas: `${API_BASE_URL}/api/transportador/alertas/alertas/`,
    
    // Integrações
    integracoes: `${API_BASE_URL}/api/transportador/integracoes/integracoes/`,
    
    // Configurações
    configuracoes: `${API_BASE_URL}/api/transportador/configuracoes/configuracoes/`,
    
    // Relatórios
    relatorios: `${API_BASE_URL}/api/transportador/relatorios/relatorios/`,
    
    // Notas Fiscais
    notasFiscais: `${API_BASE_URL}/api/transportador/notas_fiscais/notas/`,
    
    // Auditoria
    auditoria: `${API_BASE_URL}/api/transportador/auditoria/logs/`,
    
    // Empresas e Filiais
    empresas: `${API_BASE_URL}/api/transportador/empresas/empresas/`,
    filiais: `${API_BASE_URL}/api/transportador/empresas/filiais/`,
    
    // Motoristas
    motoristasInternos: `${API_BASE_URL}/api/transportador/motorista-interno/motoristas/`,
    motoristasExternos: `${API_BASE_URL}/api/transportador/motorista-externo/motoristas-externos/`,
    vinculosMotorista: `${API_BASE_URL}/api/transportador/motorista-interno/vinculos/`,
    jornadasMotorista: `${API_BASE_URL}/api/transportador/motorista-interno/jornadas/`,
    mensagensMotorista: `${API_BASE_URL}/api/transportador/motorista-interno/mensagens/`,
    alertasMotorista: `${API_BASE_URL}/api/transportador/motorista-interno/alertas/`,
    alocacoesMotorista: `${API_BASE_URL}/api/transportador/motorista-externo/alocacoes-motorista/`,
    
    // Clientes
    clientes: `${API_BASE_URL}/api/transportador/clientes/clientes/`,
    contatosClientes: `${API_BASE_URL}/api/transportador/clientes/contatos/`,
    
    // Fornecedores
    fornecedores: `${API_BASE_URL}/api/transportador/fornecedores/fornecedores/`,
    contatosFornecedores: `${API_BASE_URL}/api/transportador/fornecedores/contatos/`,
    
    // Viagens
    viagens: `${API_BASE_URL}/api/transportador/viagens/viagens/`,
    cargasViagem: `${API_BASE_URL}/api/transportador/viagens/cargas/`,
    paradasViagem: `${API_BASE_URL}/api/transportador/viagens/paradas/`,
    
    // Entregas
    entregas: `${API_BASE_URL}/api/transportador/entregas/entregas/`,
    pods: `${API_BASE_URL}/api/transportador/entregas/pods/`,
    ocorrenciasEntregas: `${API_BASE_URL}/api/transportador/entregas/ocorrencias/`,
    tentativasEntregas: `${API_BASE_URL}/api/transportador/entregas/tentativas/`,
    
    // Combustível
    postosCombustivel: `${API_BASE_URL}/api/transportador/combustivel/postos/`,
    abastecimentos: `${API_BASE_URL}/api/transportador/combustivel/abastecimentos/`,
    consumoMensal: `${API_BASE_URL}/api/transportador/combustivel/consumo-mensal/`,
    
    // Multas
    multas: `${API_BASE_URL}/api/transportador/multas/multas/`,
    recursosMultas: `${API_BASE_URL}/api/transportador/multas/recursos/`,
    pontuacaoCNH: `${API_BASE_URL}/api/transportador/multas/pontuacao-cnh/`,
    
    // Contratos
    contratos: `${API_BASE_URL}/api/transportador/contratos/contratos/`,
    aditivosContratos: `${API_BASE_URL}/api/transportador/contratos/aditivos/`,
    
    // Custos
    categoriasCustos: `${API_BASE_URL}/api/transportador/custos/categorias/`,
    custos: `${API_BASE_URL}/api/transportador/custos/custos/`,
    custoPorKm: `${API_BASE_URL}/api/transportador/custos/custo-por-km/`,
    
    // Pagamentos
    contasPagar: `${API_BASE_URL}/api/transportador/pagamentos/contas-pagar/`,
    contasReceber: `${API_BASE_URL}/api/transportador/pagamentos/contas-receber/`,
    pagamentos: `${API_BASE_URL}/api/transportador/pagamentos/pagamentos/`,
    
    // Rastreamento
    posicoesRastreamento: `${API_BASE_URL}/api/transportador/rastreamento/posicoes/`,
    cercasEletronicas: `${API_BASE_URL}/api/transportador/rastreamento/cercas/`,
    violacoesCercas: `${API_BASE_URL}/api/transportador/rastreamento/violacoes/`,
    historicoRastreamento: `${API_BASE_URL}/api/transportador/rastreamento/historico/`,
  },
};

export default API_ENDPOINTS;

