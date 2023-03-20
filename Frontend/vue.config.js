const { defineConfig } = require('@vue/cli-service');

// module.exports = defineConfig({
//   transpileDependencies: true,
// });

const NodePolyfillPlugin = require("node-polyfill-webpack-plugin");

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    plugins: [new NodePolyfillPlugin()],
  },
  // configureWebpack: {
    // resolve: {
    //   fallback: {
    //     // os: false,
    //     // path: false,
    //     os: require.resolve("os-browserify/browser"),
    //     path: require.resolve("path-browserify"),
    //   },
    // },
  // },
});
