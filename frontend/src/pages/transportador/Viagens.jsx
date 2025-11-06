import createResourceListPage from './shared/createResourceListPage';

export default createResourceListPage({
  title: 'Viagens',
  description: 'Integração com o módulo de viagens: cargas, rotas planejadas e paradas executadas.',
  endpoints: [
    '/api/transportador/viagens/viagens/',
    '/api/transportador/viagens/cargas/',
    '/api/transportador/viagens/paradas/',
  ],
});
