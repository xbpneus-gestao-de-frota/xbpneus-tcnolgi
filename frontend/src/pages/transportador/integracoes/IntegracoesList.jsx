import createResourceListPage from '../shared/createResourceListPage';

export default createResourceListPage({
  title: 'Integrações',
  description: 'Gerencie integrações externas, credenciais de API e webhooks configurados.',
  endpoints: [
    '/api/transportador/integracoes/integracaoexternas/',
    '/api/transportador/integracoes/apicredentials/',
    '/api/transportador/integracoes/webhookconfigs/',
    '/api/transportador/integracoes/logintegracaos/',
  ],
});
