const axios = require('axios');

async function makeApiRequest(url, method = 'GET', headers = {}, params = {}, data = {}) {
    try {
        const response = await axios({
            method,
            url,
            headers,
            params,
            data
        });
        
        return {
            statusCode: response.status,
            headers: response.headers,
            content: response.data
        };
    } catch (error) {
        if (error.response) {
            return {
                statusCode: error.response.status,
                headers: error.response.headers,
                content: error.response.data
            };
        }
        return { error: error.message };
    }
}

module.exports = { makeApiRequest };
