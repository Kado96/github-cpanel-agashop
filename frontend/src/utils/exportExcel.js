/**
 * @file exportExcel.js
 * @description Utilitaire centralisé pour l'export Excel, compatible Web ET Android (Capacitor).
 * Sur Android WebView, <a download> est ignoré. On utilise donc Capacitor Filesystem
 * pour écrire le fichier sur le disque puis Capacitor Share pour le partager.
 * @author Kora Agency
 */
import * as XLSX from 'xlsx';
import { Capacitor } from '@capacitor/core';

/**
 * Exporte un workbook XLSX vers un fichier téléchargeable.
 * - Sur Web : utilise un lien <a> avec Blob pour déclencher le téléchargement.
 * - Sur Android/iOS : écrit le fichier via Filesystem puis ouvre le dialogue de partage.
 *
 * @param {Object} wb - Le workbook XLSX généré par XLSX.utils.book_new()
 * @param {string} fileName - Le nom du fichier (ex: "Ventes_2026-01-01.xlsx")
 */
export async function saveWorkbook(wb, fileName) {
  try {
    // Générer le fichier en tant que tableau d'octets
    const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });

    if (Capacitor.isNativePlatform()) {
      // === MODE ANDROID / iOS (Capacitor) ===
      // Importer dynamiquement pour éviter les erreurs sur Web
      const { Filesystem, Directory } = await import('@capacitor/filesystem');
      const { Share } = await import('@capacitor/share');

      // Convertir le ArrayBuffer en base64
      const uint8 = new Uint8Array(wbout);
      let binary = '';
      for (let i = 0; i < uint8.length; i++) {
        binary += String.fromCharCode(uint8[i]);
      }
      const base64Data = btoa(binary);

      // Écrire le fichier dans le répertoire Cache (pas besoin de permissions)
      const result = await Filesystem.writeFile({
        path: fileName,
        data: base64Data,
        directory: Directory.Cache
      });

      // Partager le fichier (ouvre le dialogue Android : Gmail, Drive, WhatsApp...)
      await Share.share({
        title: fileName,
        text: `Export AgaShop : ${fileName}`,
        url: result.uri,
        dialogTitle: 'Exporter le fichier Excel'
      });

    } else {
      // === MODE WEB (Navigateur standard) ===
      const blob = new Blob([wbout], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      });

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

    // Fallback ultime : essayer l'approche Blob même sur native
    try {
      const blob = new Blob([XLSX.write(wb, { bookType: 'xlsx', type: 'array' })], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      });
      const url = URL.createObjectURL(blob);
      window.open(url, '_blank');
      setTimeout(() => URL.revokeObjectURL(url), 5000);
    } catch (fallbackError) {
      console.error('[ExportExcel] Fallback aussi échoué:', fallbackError);
      throw error;
    }
  }
}
