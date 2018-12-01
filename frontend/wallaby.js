module.exports = function (wallaby) {
  const compiler = wallaby.compilers.babel({
    'presets': [
      ['vue-app', { 'useBuiltIns': true }],
      'stage-2'
    ],
    'plugins': [
      'transform-class-properties'
    ]
  });

  return {
    files: [
      // loading kendo globally
      // { pattern: 'node_modules/@progress/kendo-ui/js/kendo.all.js', instrument: false },
      { pattern: 'node_modules/vue/dist/vue.js', instrument: false },
      { pattern: 'node_modules/babel-polyfill/dist/polyfill.js', instrument: false },
      { pattern: 'assets/**/*.png' },
      { pattern: 'assets/**/*.ttf' },
      { pattern: 'components/**/*.vue' },
      { pattern: 'layout/**/*.vue' },
      { pattern: 'pages/**/*.vue' },
      { pattern: 'services/**/*.vue' },
      { pattern: 'store/**/*.vue' },
      { pattern: 'components/**/*.ts' },
      { pattern: 'enuns/**/*.ts' },
      { pattern: 'layout/**/*.ts' },
      { pattern: 'pages/**/*.ts' },
      { pattern: 'pages/**/*.json' },
      { pattern: 'services/**/*.ts' },
      { pattern: 'store/**/*.ts' }
    ],

    tests: [
      './components/**/*.spec.js',
      './store/**/*.spec.js',
      './tests/**/*.spec.js'
    ],

    env: {
      type: 'node',
      runner: 'node',
      params: { env: 'wallaby=true' }
    },

    hints: {
      ignoreCoverage: /ignore coverage/
    },

    compilers: {
      '**/*.js': compiler,
      '**/*.vue': require('wallaby-vue-compiler')(compiler)
    },

    preprocessors: {
      '**/*.vue': file => require('jest-vue-preprocessor').process(file.content, file.path)
    },

    testFramework: 'jest',

    setup: function () {
      const jestConfig = require('./package.json').jest || require('./jest.config');
      jestConfig.moduleNameMapper = {
        '^~/(.*)$': wallaby.projectCacheDir + '$1'
      };
      jestConfig.transform = {};
      wallaby.testFramework.configure(jestConfig);
    },

    debug: true
  };
};
