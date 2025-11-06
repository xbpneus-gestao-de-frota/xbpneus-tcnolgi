import createResourceListPage from '../shared/createResourceListPage';

export default createResourceListPage({
  title: 'EPIs',
  description: 'Gerencie tipos de EPI, entregas e fichas de controle dos colaboradores.',
  endpoints: [
    '/api/transportador/epis/epis/',
    '/api/transportador/epis/entregaepis/',
    '/api/transportador/epis/fichaepis/',
    '/api/transportador/epis/tipoepis/',
  ],
});
