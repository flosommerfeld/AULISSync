// webpack.config.js:

var path = require("path");
var CopyPlugin = require("copy-webpack-plugin");

module.exports = {
  mode: "development",
  resolve: {
    extensions: ["", ".js", ".jsx"]
  },
  entry: [
    path.resolve(__dirname, "src/gui/index.jsx")
  ],
  output: {
    path: path.resolve(__dirname, "public/dist"),
    filename: "main.js",
    publicPath: "dist/"
  },
  devServer: {
    static: {
      directory: path.join(__dirname, "public/dist"),
    },
    compress: true,
    port: 9000,
    // the middleware enables our server to reload on changes
    devMiddleware: {
      index: true,
      mimeTypes: { "text/html": ["phtml"] },
      publicPath: "/public/dist",
      serverSideRender: true,
      writeToDisk: true,
    },
  },
  module: {
    rules: [
      {
        test: /\.(jsx|js)$/,
        include: path.resolve(__dirname, "src"),
        exclude: /node_modules/,
        use: [{
          loader: "babel-loader",
          options: {
            presets: [
              ["@babel/preset-env", {
                "targets": "defaults"
              }],
              "@babel/preset-react"
            ]
          }
        }]
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      }, {
        test: /\.(png|j?g|svg|gif)?$/,
        use: "file-loader"
      }
    ]
  },
  plugins: [
    new CopyPlugin({
      patterns: [
        // copy our static assets to the public folder so that they are available for our dev server 
        { from: path.resolve(__dirname, "src/gui/styles"), to: path.resolve(__dirname, "public/dist/styles") },
        { from: path.resolve(__dirname, "src/gui/index.html"), to: path.resolve(__dirname, "public/dist/index.html"), toType: "file" },
        { from: path.resolve(__dirname, "src/gui/routes/login.html"), to: path.resolve(__dirname, "public/dist/login/index.html"), toType: "file" },
        { from: path.resolve(__dirname, "src/gui/routes/settings.html"), to: path.resolve(__dirname, "public/dist/settings/index.html"), toType: "file" },
      ]
    }),
  ],
}
