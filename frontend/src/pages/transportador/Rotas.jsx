import createResourceListPage from './shared/createResourceListPage';

export default createResourceListPage({
  title: 'Rotas',
  description: 'Planejamento de rotas, pontos e otimizações calculadas pelo backend.',
  endpoints: [
    '/api/transportador/rotas/rotas/',
    '/api/transportador/rotas/otimizadas/',
    '/api/transportador/rotas/pontos/',
  ],
});
