const fs = require('fs').promises;
const path = require('path');

async function loadConfig(configPath) {
    try {
        const data = await fs.readFile(configPath, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        throw new Error(`Failed to load config: ${error.message}`);
    }
}

module.exports = { loadConfig };
