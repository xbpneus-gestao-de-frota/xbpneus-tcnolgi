import createResourceListPage from './shared/createResourceListPage';

export default createResourceListPage({
  title: 'Multas e Penalidades',
  description: 'Visualize multas registradas, recursos enviados e controle de pontuação de CNH providos pelo backend.',
  endpoints: [
    '/api/transportador/multas/multas/',
    '/api/transportador/multas/recursos/',
    '/api/transportador/multas/pontuacao-cnh/',
  ],
});
