import createResourceListPage from './shared/createResourceListPage';

export default createResourceListPage({
  title: 'Entregas',
  description: 'Acompanhe entregas, comprovantes (PODs) e ocorrências registradas em rota.',
  endpoints: [
    '/api/transportador/entregas/entregas/',
    '/api/transportador/entregas/pods/',
    '/api/transportador/entregas/ocorrencias/',
    '/api/transportador/entregas/tentativas/',
  ],
});
