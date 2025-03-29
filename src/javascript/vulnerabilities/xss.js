const { makeApiRequest } = require('../core/utils');

async function check(targetUrl, config) {
    const testPayloads = config?.xss?.test_payloads || [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "\"><script>alert('XSS')</script>"
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
                vulnerable: response.content?.includes(payload)
            });
        }
    }
    
    return {
        name: "Cross-Site Scripting (XSS)",
        description: "Tests for XSS vulnerabilities",
        results,
        severity: "Medium"
    };
}

module.exports = { check };
