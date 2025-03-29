const { check: sqlInjectionCheck } = require('../vulnerabilities/sqlInjection');
const { check: xssCheck } = require('../vulnerabilities/xss');
const { check: brokenAuthCheck } = require('../vulnerabilities/brokenAuth');
const { check: sensitiveDataCheck } = require('../vulnerabilities/sensitiveData');
const { check: rateLimitingCheck } = require('../vulnerabilities/rateLimiting');

class APIScanner {
    constructor(targetUrl, config) {
        this.targetUrl = targetUrl;
        this.config = config;
        this.checks = [
            sqlInjectionCheck,
            xssCheck,
            brokenAuthCheck,
            sensitiveDataCheck,
            rateLimitingCheck
        ];
    }

    async runScan() {
        const results = {
            target: this.targetUrl,
            timestamp: new Date().toISOString(),
            vulnerabilities: []
        };

        for (const check of this.checks) {
            try {
                const result = await check(this.targetUrl, this.config);
                results.vulnerabilities.push(result);
            } catch (error) {
                console.error(`Error running ${check.name}: ${error.message}`);
            }
        }

        return results;
    }
}

module.exports = { APIScanner };
