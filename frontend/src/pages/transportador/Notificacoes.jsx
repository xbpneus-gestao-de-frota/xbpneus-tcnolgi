import createResourceListPage from './shared/createResourceListPage';

export default createResourceListPage({
  title: 'Notificações',
  description: 'Gerencie canais, templates e notificações disparadas pelo sistema.',
  endpoints: [
    '/api/transportador/notificacoes/notificacoes/',
    '/api/transportador/notificacoes/canais/',
    '/api/transportador/notificacoes/templates/',
    '/api/transportador/notificacoes/preferencias/',
  ],
});
