module.exports = {
  testEnvironment: 'jsdom',
  transform: { '^.+\\.js$': 'babel-jest', '^.+\\.vue$': '@vue/vue3-jest' },
  moduleFileExtensions: ['js', 'json', 'vue'],
  moduleNameMapper: {
    '^\\.\\./api$': '<rootDir>/src/api/api-component-mock.cjs',
    '^\\.\\./api/kakao$': '<rootDir>/src/api/kakao-component-mock.cjs',
    '^\\.\\./router/index\\.js$': '<rootDir>/src/router/router-component-mock.cjs',
    '^\\.\\./stores/session\\.js$': '<rootDir>/src/stores/session-component-mock.cjs',
    '^vue$': 'vue/dist/vue.cjs.js',
    '^@vue/test-utils$': '<rootDir>/node_modules/@vue/test-utils/dist/vue-test-utils.cjs.js',
    '^@vue/compiler-dom$': '@vue/compiler-dom/dist/compiler-dom.cjs.js',
    '^@vue/compiler-core$': '@vue/compiler-core/dist/compiler-core.cjs.js',
  },
}
