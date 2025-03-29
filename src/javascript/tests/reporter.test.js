const fs = require('fs').promises;
const { generateReport } = require('../core/reporter');

jest.mock('fs', () => ({
  promises: {
    mkdir: jest.fn().mockResolvedValue(true),
    writeFile: jest.fn().mockResolvedValue(true)
  }
}));

describe('Reporter', () => {
  const sampleResults = {
    target: "http://test.com",
    vulnerabilities: []
  };

  test('generateReport creates report file', async () => {
    const reportPath = await generateReport(sampleResults, "test_reports");
    expect(fs.promises.mkdir).toHaveBeenCalled();
    expect(fs.promises.writeFile).toHaveBeenCalled();
    expect(reportPath).toContain("api_scan_report");
  });
});
