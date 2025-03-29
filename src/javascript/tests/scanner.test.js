const { APIScanner } = require('../core/scanner');
const { makeApiRequest } = require('../core/utils');

jest.mock('../core/utils');

describe('APIScanner', () => {
  const mockConfig = {
    sql_injection: {
      test_payloads: ["test_payload"]
    }
  };

  beforeEach(() => {
    makeApiRequest.mockReset();
  });

  test('runScan executes vulnerability checks', async () => {
    makeApiRequest.mockResolvedValue({
      statusCode: 200,
      content: "test response"
    });

    const scanner = new APIScanner("http://test.com", mockConfig);
    const results = await scanner.runScan();
    
    expect(results.vulnerabilities.length).toBeGreaterThan(0);
    expect(makeApiRequest).toHaveBeenCalled();
  });
});
