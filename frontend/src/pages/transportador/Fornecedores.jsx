import createResourceListPage from './shared/createResourceListPage';

export default createResourceListPage({
  title: 'Fornecedores',
  description: 'Consulte fornecedores homologados e seus pontos de contato expostos pelo backend.',
  endpoints: [
    '/api/transportador/fornecedores/fornecedores/',
    '/api/transportador/fornecedores/contatos/',
  ],
});
