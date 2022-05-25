module.exports = {
    preset: 'ts-jest',
    testEnvironment: 'node',
    testPathIgnorePatterns: ['<rootDir>/test/fixtures'],
    coveragePathIgnorePatterns: ['<rootDir>/test/'],
    testRegex: 'test/(.+)\\.test\\.(jsx?|tsx?)$',
    setupFilesAfterEnv: ['./jest.setup.js'],
};