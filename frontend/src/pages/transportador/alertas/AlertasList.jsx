import createResourceListPage from '../shared/createResourceListPage';

export default createResourceListPage({
  title: 'Alertas',
  description: 'Monitore alertas configurados, históricos de disparo e categorias disponíveis.',
  endpoints: [
    '/api/transportador/alertas/alertas/',
    '/api/transportador/alertas/historicoalertas/',
    '/api/transportador/alertas/tipoalertas/',
    '/api/transportador/alertas/configuracaoalertas/',
  ],
});
