import createResourceListPage from './shared/createResourceListPage';

export default createResourceListPage({
  title: 'Contratos',
  description: 'Gestão de contratos e aditivos vinculados a clientes e fornecedores.',
  endpoints: [
    '/api/transportador/contratos/contratos/',
    '/api/transportador/contratos/aditivos/',
  ],
});
