/**
 * Configuração de permissões e rotas por tipo de usuário (role)
 */

export const ROLES = {
  TRANSPORTADOR: 'transportador',
  MOTORISTA: 'motorista',
  REVENDA: 'revenda',
  BORRACHARIA: 'borracharia',
  RECAPAGEM: 'recapagem',
};

/**
 * Define quais rotas cada tipo de usuário pode acessar
 */
export const ROLE_PERMISSIONS = {
  [ROLES.TRANSPORTADOR]: {
    dashboard: '/dashboard',
    routes: ['/dashboard', '/frota', '/pneus', '/estoque', '/manutencao', '/motoristas', '/relatorios'],
    label: 'Transportador',
  },
  [ROLES.MOTORISTA]: {
    dashboard: '/motorista/dashboard',
    routes: ['/motorista/dashboard', '/motorista/veiculo', '/motorista/viagens', '/motorista/manutencoes'],
    label: 'Motorista',
  },
  [ROLES.REVENDA]: {
    dashboard: '/revenda/dashboard',
    routes: ['/revenda/dashboard', '/revenda/estoque', '/revenda/vendas', '/revenda/clientes'],
    label: 'Revenda',
  },
  [ROLES.BORRACHARIA]: {
    dashboard: '/borracharia/dashboard',
    routes: ['/borracharia/dashboard', '/borracharia/servicos', '/borracharia/clientes', '/borracharia/estoque'],
    label: 'Borracharia',
  },
  [ROLES.RECAPAGEM]: {
    dashboard: '/recapagem/dashboard',
    routes: ['/recapagem/dashboard', '/recapagem/pneus', '/recapagem/processos', '/recapagem/clientes'],
    label: 'Recapagem',
  },
};

/**
 * Verifica se o usuário tem permissão para acessar uma rota
 */
export const hasPermission = (userRole, route) => {
  const permissions = ROLE_PERMISSIONS[userRole];
  if (!permissions) return false;
  return permissions.routes.includes(route);
};

/**
 * Retorna o dashboard padrão para o tipo de usuário
 */
export const getDefaultDashboard = (userRole) => {
  const permissions = ROLE_PERMISSIONS[userRole];
  return permissions?.dashboard || '/dashboard';
};

/**
 * Retorna o label do tipo de usuário
 */
export const getRoleLabel = (userRole) => {
  const permissions = ROLE_PERMISSIONS[userRole];
  return permissions?.label || 'Usuário';
};

