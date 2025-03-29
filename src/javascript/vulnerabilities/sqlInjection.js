const { makeApiRequest } = require('../core/utils');

async function check(targetUrl, config) {
    const testPayloads = config?.sql_injection?.test_payloads || [
        "' OR '1'='1",
        "' OR 1=1--",
        "admin'--"
    ];
    
    const results = [];
    for (const payload of testPayloads) {
        const response = await makeApiRequest(
            `${targetUrl}?input=${encodeURIComponent(payload)}`,
            'GET'
        );
        
        if (response.error) {
            results.push({
                payload,
                error: response.error
            });
        } else {
            results.push({
                payload,
                statusCode: response.statusCode,
                vulnerable: response.content?.toLowerCase().includes('sql')
            });
        }
    }
    
    return {
        name: "SQL Injection",
        description: "Tests for SQL injection vulnerabilities",
        results,
        severity: "High"
    };
}

module.exports = { check };
