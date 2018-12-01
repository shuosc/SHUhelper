module.exports = {
  moduleFileExtensions: [
    'ts',
    'tsx',
    'js',
    'jsx',
    'json',
    'vue'
  ],

  transform: {
    '^.+\\.vue$': 'vue-jest',
    '.+\\.(css|styl|less|sass|scss|png|jpg|ttf|woff|woff2)$': 'jest-transform-stub',
    '^.+\\.(ts|js)x?$': 'ts-jest'
  },

  moduleNameMapper: {
    '^~/(.*)$': '<rootDir>/$1',
    '^vue$': 'vue/dist/vue.common.js'
  },

  snapshotSerializers: [
    'jest-serializer-vue'
  ],

  setupFiles: [
    '<rootDir>/tests/unit/setup.ts'
  ],

  coverageDirectory: '<rootDir>/tests/unit/coverage',

  collectCoverageFrom: [
    'components/**/*.{js,ts,vue}',
    'layouts/**/*.{js,ts,vue}',
    'pages/**/*.{js,ts,vue}',
    'store/**/*.{js,ts}',
    '!**/node_modules/**'
  ],

  testPathIgnorePatterns: [
    '<rootDir>/tests/e2e'
  ],

  testMatch: [
    '**/*.spec.(js|ts)'
  ]
};
