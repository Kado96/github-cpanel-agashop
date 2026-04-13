/**
 * @file exportExcel.js
 * @description Utilitaire centralisé pour l'export Excel, compatible Web ET Android (Capacitor).
 * Remplace XLSX.writeFile() qui ne fonctionne pas dans une WebView Android.
 * @author Kora Agency
 */
import * as XLSX from 'xlsx';
import { Capacitor } from '@capacitor/core';

/**
 * Exporte un workbook XLSX vers un fichier téléchargeable.
 * - Sur Web : utilise un lien <a> avec Blob pour déclencher le téléchargement.
 * - Sur Android/iOS : utilise un lien <a> avec Blob + window.open en fallback.
 *
 * @param {Object} wb - Le workbook XLSX généré par XLSX.utils.book_new()
 * @param {string} fileName - Le nom du fichier (ex: "Ventes_2026-01-01.xlsx")
 */
export function saveWorkbook(wb, fileName) {
  try {
    // Générer le fichier en tant que tableau d'octets
    const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });

    // Créer un Blob à partir du tableau d'octets
    const blob = new Blob([wbout], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    });

    if (Capacitor.isNativePlatform()) {
      // === MODE ANDROID / iOS (Capacitor) ===
      // Utiliser FileReader pour convertir le Blob en data URL
      const reader = new FileReader();
      reader.onloadend = function () {
        const dataUrl = reader.result;
        // Créer un lien temporaire pour déclencher le téléchargement
        const link = document.createElement('a');
        link.href = dataUrl;
        link.download = fileName;
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();

        // Nettoyage après un court délai
        setTimeout(() => {
          document.body.removeChild(link);
        }, 300);
      };
      reader.readAsDataURL(blob);
    } else {
      // === MODE WEB (Navigateur standard) ===
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = fileName;
      link.style.display = 'none';
      document.body.appendChild(link);
      link.click();

      // Nettoyage
      setTimeout(() => {
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      }, 300);
    }
  } catch (error) {
    console.error('[ExportExcel] Erreur lors de l\'export:', error);
    throw error;
  }
}
