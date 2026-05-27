/**
 * GKT NPS — Receptor de respostas
 *
 * Como usar:
 * 1. Crie uma planilha nova no Google Sheets (ex: "GKT NPS — Imersão Legado")
 * 2. Menu Extensões → Apps Script
 * 3. Apague o código padrão, cole este arquivo inteiro
 * 4. Salve (disquete ou Cmd+S)
 * 5. Clique em "Implantar" → "Nova implantação"
 *    - Tipo: Aplicativo da Web
 *    - Executar como: Eu
 *    - Quem tem acesso: Qualquer pessoa
 *    - Implantar → autorize quando pedir
 * 6. Copie a URL gerada (termina com /exec) e cole no index.html na constante WEBHOOK_URL
 */

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // Cria cabeçalho na primeira execução
    if (sheet.getLastRow() === 0) {
      const headers = buildHeaders(data.responses);
      sheet.appendRow(headers);
      sheet.getRange(1, 1, 1, headers.length).setFontWeight('bold');
      sheet.setFrozenRows(1);
    }

    // Pega cabeçalho atual e adiciona colunas novas se aparecerem
    const currentHeaders = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    const incomingKeys = Object.keys(data.responses);
    const newKeys = incomingKeys.filter(k => !currentHeaders.includes(k));
    if (newKeys.length > 0) {
      newKeys.forEach(k => {
        sheet.getRange(1, sheet.getLastColumn() + 1).setValue(k).setFontWeight('bold');
      });
    }

    // Monta linha alinhada ao cabeçalho
    const finalHeaders = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    const row = finalHeaders.map(h => {
      if (h === 'submittedAt') return data.submittedAt;
      if (h === 'startedAt') return data.startedAt;
      if (h === 'event') return data.event;
      if (h === 'userAgent') return data.userAgent;
      return data.responses[h] ?? '';
    });
    sheet.appendRow(row);

    return ContentService
      .createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function buildHeaders(responses) {
  return ['submittedAt', 'startedAt', 'event', 'userAgent', ...Object.keys(responses)];
}

function doGet() {
  return ContentService
    .createTextOutput('GKT NPS receiver — ativo')
    .setMimeType(ContentService.MimeType.TEXT);
}
