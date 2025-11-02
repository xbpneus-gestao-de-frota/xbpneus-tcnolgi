export default function StatusBadge({ status, variant = 'default' }) {
  const variants = {
    success: 'bg-green-100 text-green-800 border-green-200',
    warning: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    danger: 'bg-red-100 text-red-800 border-red-200',
    info: 'bg-blue-100 text-blue-800 border-blue-200',
    default: 'bg-gray-100 text-gray-800 border-gray-200'
  };

  const statusVariants = {
    ativo: 'success',
    inativo: 'danger',
    pendente: 'warning',
    aprovado: 'success',
    rejeitado: 'danger',
    em_andamento: 'info',
    concluido: 'success',
    cancelado: 'danger',
    agendado: 'info'
  };

  const variantClass = variants[statusVariants[status?.toLowerCase()] || variant] || variants.default;

  return (
    <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border ${variantClass}`}>
      {status}
    </span>
  );
}

