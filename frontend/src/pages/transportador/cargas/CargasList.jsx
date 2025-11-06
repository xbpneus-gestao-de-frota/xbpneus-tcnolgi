import createResourceListPage from '../shared/createResourceListPage';

export default createResourceListPage({
  title: 'Cargas',
  description: 'Controle cargas, manifestos e rastreamento diretamente do backend.',
  endpoints: [
    '/api/transportador/cargas/cargas/',
    '/api/transportador/cargas/manifestocargas/',
    '/api/transportador/cargas/rastreamentocargas/',
    '/api/transportador/cargas/itemcargas/',
    '/api/transportador/cargas/tipocargas/',
  ],
});
