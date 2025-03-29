const { makeApiRequest } = require('../core/utils');

async function check(targetUrl, config) {
    const endpointsToCheck = config?.sensitive_data?.endpoints || [
        "/users",
        "/profile",
        "/account"
    ];
    
    const results = [];
    for (const endpoint of endpointsToCheck) {
        const response = await makeApiRequest(
            `${targetUrl}${endpoint}`,
            'GET'
        );
        
        if (response.error) {
            results.push({
                endpoint,
                error: response.error
            });
        } else {
            const sensitiveFields = [];
            const content = JSON.stringify(response.content || '');
            
            if (content.includes('password')) sensitiveFields.push('password');
            if (content.includes('credit_card')) sensitiveFields.push('credit_card');
            if (content.includes('ssn')) sensitiveFields.push('ssn');
            
            results.push({
                endpoint,
                statusCode: response.statusCode,
                sensitiveDataExposed: sensitiveFields.length > 0,
                fieldsFound: sensitiveFields
            });
        }
    }
    
    return {
        name: "Sensitive Data Exposure",
        description: "Checks for exposed sensitive data",
        results,
        severity: "High"
    };
}

module.exports = { check };
