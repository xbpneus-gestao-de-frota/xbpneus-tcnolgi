/**
 * Configuração de Cores - Sistema XBPneus
 * Baseado no padrão das telas de Login e Cadastro
 */

export const xbpneusColors = {
  // Cores principais do degradê do logo
  primary: {
    light: '#60a5fa',    // blue-400
    DEFAULT: '#6366f1',  // indigo-500
    dark: '#7c3aed',     // purple-600
  },
  
  // Azul marinho escuro (uniforme dos mascotes, sidebar)
  navy: {
    DEFAULT: '#1A237E',
    light: '#3949AB',
    dark: '#0D1642',
  },
  
  // Cores para inputs (bordas coloridas)
  input: {
    green: '#4CAF50',
    blue: '#5B7FE8',
    orange: '#FFA726',
    purple: '#9C27B0',
    cyan: '#00BCD4',
    pink: '#E91E63',
    darkPurple: '#673AB7',
  },
  
  // Cores de status
  status: {
    success: '#4CAF50',
    warning: '#FFA726',
    error: '#E91E63',
    info: '#00BCD4',
    neutral: '#9E9E9E',
  },
  
  // Cores de texto
  text: {
    primary: '#1A237E',    // Azul escuro
    secondary: '#666666',  // Cinza médio
    light: '#BDBDBD',      // Cinza claro (placeholder)
    white: '#FFFFFF',
  },
  
  // Cores de fundo
  background: {
    light: '#F5F5F5',      // Fundo geral
    white: '#FFFFFF',      // Cards
    gray: '#FAFAFA',       // Alternativo
  },
  
  // Cores de borda
  border: {
    light: '#E0E0E0',
    DEFAULT: '#BDBDBD',
    dark: '#9E9E9E',
  },
};

/**
 * Classes Tailwind prontas para uso
 */
export const xbpneusClasses = {
  // Degradê do logo/título
  logoGradient: 'bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600',
  logoText: 'bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 bg-clip-text text-transparent',
  
  // Botões primários
  buttonPrimary: 'bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 text-white hover:opacity-90 disabled:opacity-50 shadow-lg',
  buttonSecondary: 'border-2 border-blue-500 text-blue-500 hover:bg-blue-50',
  
  // Sidebar
  sidebarBg: 'bg-[#1A237E]',
  sidebarText: 'text-white',
  sidebarActive: 'bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600',
  sidebarHover: 'hover:bg-[#3949AB]',
  
  // Header
  headerBg: 'bg-white shadow-md',
  headerText: 'text-[#1A237E]',
  headerIcon: 'text-blue-500',
  
  // Cards
  card: 'bg-white rounded-xl shadow-md',
  cardTitle: 'text-[#1A237E] font-semibold',
  
  // Inputs
  input: 'border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 text-blue-900',
  inputLabel: 'text-gray-700 font-medium',
  
  // Tabelas
  tableHeader: 'bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 text-white',
  tableRow: 'hover:bg-blue-50',
  tableRowAlt: 'bg-gray-50',
  
  // Links
  link: 'text-blue-700 hover:text-blue-800 underline',
  
  // Badges/Status
  badgeSuccess: 'bg-green-100 text-green-800 border border-green-300',
  badgeWarning: 'bg-orange-100 text-orange-800 border border-orange-300',
  badgeError: 'bg-red-100 text-red-800 border border-red-300',
  badgeInfo: 'bg-cyan-100 text-cyan-800 border border-cyan-300',
};

/**
 * Estilos inline para componentes que não usam Tailwind
 */
export const xbpneusStyles = {
  logoGradient: {
    background: 'linear-gradient(135deg, #60a5fa, #6366f1, #7c3aed)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text',
    textShadow: '4px 4px 12px rgba(0,0,0,0.5)',
  },
  
  buttonPrimary: {
    background: 'linear-gradient(to right, #60a5fa, #6366f1, #7c3aed)',
    color: '#ffffff',
    boxShadow: '0 4px 6px rgba(99, 102, 241, 0.3)',
  },
  
  sidebarBg: {
    backgroundColor: '#1A237E',
  },
  
  card: {
    backgroundColor: '#ffffff',
    borderRadius: '12px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
  },
};

export default {
  colors: xbpneusColors,
  classes: xbpneusClasses,
  styles: xbpneusStyles,
};

