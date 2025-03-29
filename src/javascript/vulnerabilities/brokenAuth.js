const { makeApiRequest } = require('../core/utils');

async function check(targetUrl, config) {
    const authEndpoints = config?.broken_auth?.auth_endpoints || {
        login: "/login",
        protected: "/admin"
    };
    
    const results = [];
    const weakCreds = config?.broken_auth?.test_credentials || [
        { username: "admin", password: "admin" },
        { username: "user", password: "123456" },
        { username: "test", password: "password" }
    ];
    
    for (const creds of weakCreds) {
        const response = await makeApiRequest(
            `${targetUrl}${authEndpoints.login}`,
            'POST',
            {},
            {},
            creds
        );
        
        if (response.statusCode === 200 && response.content?.token) {
            results.push({
                test: "Weak credentials accepted",
                vulnerable: true,
                credentials: creds
            });
        }
    }
    
    return {
        name: "Broken Authentication",
        description: "Tests for authentication vulnerabilities",
        results,
        severity: "High"
    };
}

module.exports = { check };
