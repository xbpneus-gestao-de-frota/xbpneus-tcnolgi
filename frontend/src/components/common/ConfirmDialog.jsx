import { AlertTriangle } from 'lucide-react';

export default function ConfirmDialog({ isOpen, onClose, onConfirm, title, message, confirmText = 'Confirmar', cancelText = 'Cancelar', variant = 'danger' }) {
  if (!isOpen) return null;

  const variantClasses = {
    danger: 'from-red-600 to-red-700 hover:from-red-700 hover:to-red-800',
    warning: 'from-yellow-600 to-yellow-700 hover:from-yellow-700 hover:to-yellow-800',
    info: 'from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800'
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div className="bg-white rounded-lg shadow-2xl w-full max-w-md mx-4">
        {/* Header */}
        <div className="flex items-center gap-4 p-6 border-b border-gray-200">
          <div className={`p-3 rounded-full ${variant === 'danger' ? 'bg-red-100' : variant === 'warning' ? 'bg-yellow-100' : 'bg-blue-100'}`}>
            <AlertTriangle size={24} className={variant === 'danger' ? 'text-red-600' : variant === 'warning' ? 'text-yellow-600' : 'text-blue-600'} />
          </div>
          <h2 className="text-xl font-bold text-gray-900">
            {title}
          </h2>
        </div>

        {/* Content */}
        <div className="p-6">
          <p className="text-gray-600">
            {message}
          </p>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end gap-3 p-6 border-t border-gray-200 bg-gray-50">
          <button
            onClick={onClose}
            className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-100 transition"
          >
            {cancelText}
          </button>
          <button
            onClick={() => {
              onConfirm();
              onClose();
            }}
            className={`px-6 py-2 bg-gradient-to-r ${variantClasses[variant]} text-white rounded-lg transition shadow-md`}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
}

