import createResourceListPage from '../shared/createResourceListPage';

export default createResourceListPage({
  title: 'Treinamentos',
  description: 'Consulte cursos, instrutores, certificados e treinamentos realizados.',
  endpoints: [
    '/api/transportador/treinamentos/treinamentorealizados/',
    '/api/transportador/treinamentos/cursotreinamentos/',
    '/api/transportador/treinamentos/certificadotreinamentos/',
    '/api/transportador/treinamentos/instrutortreinamentos/',
  ],
});
