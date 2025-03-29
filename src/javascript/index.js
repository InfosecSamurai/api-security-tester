const { APIScanner } = require('./core/scanner');
const { generateReport } = require('./core/reporter');
const { loadConfig } = require('./core/configLoader');
const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');

async function main() {
    const argv = yargs(hideBin(process.argv))
        .option('target', {
            type: 'string',
            description: 'Target API URL',
            required: true
        })
        .option('config', {
            type: 'string',
            default: 'config/config.json',
            description: 'Configuration file path'
        })
        .option('output', {
            type: 'string',
            default: 'reports',
            description: 'Output directory for reports'
        })
        .argv;

    const config = await loadConfig(argv.config);
    const scanner = new APIScanner(argv.target, config);
    
    console.log(`Starting security scan for ${argv.target}`);
    const scanResults = await scanner.runScan();
    
    console.log('Generating report...');
    const reportPath = await generateReport(scanResults, argv.output);
    console.log(`Report generated at: ${reportPath}`);
}

main().catch(console.error);
