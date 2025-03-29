const fs = require('fs').promises;
const path = require('path');

async function generateReport(scanResults, outputDir = 'reports') {
    try {
        await fs.mkdir(outputDir, { recursive: true });
        
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const reportFilename = `api_scan_report_${timestamp}.json`;
        const reportPath = path.join(outputDir, reportFilename);
        
        await fs.writeFile(reportPath, JSON.stringify(scanResults, null, 4));
        
        return reportPath;
    } catch (error) {
        throw new Error(`Failed to generate report: ${error.message}`);
    }
}

module.exports = { generateReport };
