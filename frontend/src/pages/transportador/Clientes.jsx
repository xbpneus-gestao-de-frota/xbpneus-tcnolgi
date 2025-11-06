import createResourceListPage from './shared/createResourceListPage';

export default createResourceListPage({
  title: 'Clientes',
  description: 'Integração direta com o cadastro de clientes e contatos da API do transportador.',
  endpoints: [
    '/api/transportador/clientes/clientes/',
    '/api/transportador/clientes/contatos/',
  ],
});
