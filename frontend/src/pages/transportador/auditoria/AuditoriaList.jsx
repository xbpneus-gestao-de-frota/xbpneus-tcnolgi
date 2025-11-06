import createResourceListPage from '../shared/createResourceListPage';

export default createResourceListPage({
  title: 'Auditoria',
  description: 'Consulte logs de auditoria, acessos, alterações e sessões em tempo real.',
  endpoints: [
    '/api/transportador/auditoria/logs-auditoria/',
    '/api/transportador/auditoria/logs-acesso/',
    '/api/transportador/auditoria/logs-alteracao/',
    '/api/transportador/auditoria/sessoes/',
    '/api/transportador/auditoria/configuracoes/',
  ],
});
