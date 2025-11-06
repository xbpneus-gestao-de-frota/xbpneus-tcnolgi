import createResourceListPage from './shared/createResourceListPage';

export default createResourceListPage({
  title: 'Combustível',
  description: 'Acompanhe abastecimentos, postos e séries históricas de consumo enviados pelos serviços de combustível.',
  endpoints: [
    '/api/transportador/combustivel/abastecimentos/',
    '/api/transportador/combustivel/consumo-mensal/',
    '/api/transportador/combustivel/postos/',
  ],
});
