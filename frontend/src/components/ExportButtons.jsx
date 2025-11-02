import React, { useState } from 'react';
import { Download, Printer, ChevronDown } from 'lucide-react';
import { xbpneusClasses, xbpneusColors } from '../styles/colors';

const ExportButtons = ({ onExport, onPrint, reportName = 'Relatório' }) => {
  const [showExportMenu, setShowExportMenu] = useState(false);

  const handleExport = (format) => {
    onExport(format);
    setShowExportMenu(false);
  };

  return (
    <div className="flex gap-2">
      {/* Botão de Impressão */}
      <button
        onClick={onPrint}
        className={`${xbpneusClasses.buttonSecondary} px-4 py-2 rounded-lg flex items-center gap-2 text-sm`}
        title="Imprimir relatório"
      >
        <Printer size={18} />
        Imprimir
      </button>

      {/* Botão de Exportação com Menu */}
      <div className="relative">
        <button
          onClick={() => setShowExportMenu(!showExportMenu)}
          className={`${xbpneusClasses.buttonPrimary} px-4 py-2 rounded-lg flex items-center gap-2 text-sm`}
          title="Exportar relatório"
        >
          <Download size={18} />
          Exportar
          <ChevronDown size={16} />
        </button>

        {/* Menu de Exportação */}
        {showExportMenu && (
          <div className="absolute right-0 mt-2 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-10">
            <button
              onClick={() => handleExport('pdf')}
              className="w-full text-left px-4 py-2 hover:bg-gray-100 flex items-center gap-2"
            >
              <span className="text-red-500">📄</span>
              Exportar como PDF
            </button>
            <button
              onClick={() => handleExport('csv')}
              className="w-full text-left px-4 py-2 hover:bg-gray-100 flex items-center gap-2 border-t"
            >
              <span className="text-green-500">📊</span>
              Exportar como CSV
            </button>
            <button
              onClick={() => handleExport('excel')}
              className="w-full text-left px-4 py-2 hover:bg-gray-100 flex items-center gap-2 border-t"
            >
              <span className="text-blue-500">📋</span>
              Exportar como Excel
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ExportButtons;

