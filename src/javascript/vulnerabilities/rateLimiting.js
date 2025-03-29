const { makeApiRequest } = require('../core/utils');

async function check(targetUrl, config) {
    const endpoint = config?.rate_limiting?.test_endpoint || "/api/data";
    const maxRequests = config?.rate_limiting?.max_requests || 100;
    const thresholdSeconds = config?.rate_limiting?.threshold_seconds || 10;
    
    const results = [];
    const startTime = Date.now();
    let requestCount = 0;
    let lastResponse;
    
    while ((Date.now() - startTime) < (thresholdSeconds * 1000) && requestCount < maxRequests) {
        lastResponse = await makeApiRequest(
            `${targetUrl}${endpoint}`,
            'GET'
        );
        requestCount++;
        
        if (lastResponse.statusCode === 429) {
            break;
        }
    }
    
    const timeElapsed = (Date.now() - startTime) / 1000;
    results.push({
        requestsSent: requestCount,
        timeElapsed,
        rateLimitHit: lastResponse?.statusCode === 429,
        requestsPerSecond: timeElapsed > 0 ? requestCount / timeElapsed : 0
    });
    
    return {
        name: "Rate Limiting",
        description: "Tests for rate limiting protection",
        results,
        severity: "Medium"
    };
}

module.exports = { check };
