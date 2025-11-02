/**
 * PageHeader - Componente de cabeçalho de página padronizado
 * 
 * Aplica o padrão de cores XBPneus com degradê azul-roxo
 */

export default function PageHeader({ title, subtitle, children }) {
  return (
    <div className="mb-8">
      <div className="flex items-baseline justify-between mb-2">
        <h1 
          className="text-4xl font-black"
          style={{
            background: 'linear-gradient(135deg, #60a5fa, #6366f1, #7c3aed)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
          }}
        >
          {title}
        </h1>
        {children}
      </div>
      {subtitle && (
        <p className="text-gray-600 text-lg">{subtitle}</p>
      )}
    </div>
  );
}

