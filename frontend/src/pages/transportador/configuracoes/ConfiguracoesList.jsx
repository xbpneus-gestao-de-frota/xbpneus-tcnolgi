import createResourceListPage from '../shared/createResourceListPage';

export default createResourceListPage({
  title: 'Configurações',
  description: 'Veja parâmetros de empresa, perfis e catálogos auxiliares utilizados na operação.',
  endpoints: [
    '/api/transportador/configuracoes/configuracaosistemas/',
    '/api/transportador/configuracoes/parametroempresas/',
    '/api/transportador/configuracoes/perfilusuarios/',
    '/api/transportador/configuracoes/permissaocustomizadas/',
    '/api/transportador/configuracoes/catalogo-modelos-veiculos/',
    '/api/transportador/configuracoes/mapa-posicoes-pneus/',
    '/api/transportador/configuracoes/operacoes-configuracoes/',
    '/api/transportador/configuracoes/medidas-por-posicao/',
    '/api/transportador/configuracoes/pressoes-recomendadas/',
    '/api/transportador/configuracoes/catalogo-pneus-xbri/',
  ],
});
