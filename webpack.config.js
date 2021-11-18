// webpack.config.js:

var path = require('path');
var webpack = require('webpack');

module.exports = {
  mode: 'development',
  resolve: {
    extensions: ['', '.js', '.jsx']
  },
  entry:  [
    path.resolve(__dirname, 'src/gui/index.jsx')
  ],
  output: {
    path: path.resolve(__dirname, 'public/dist'),
    filename: 'main.js',
    publicPath: 'dist/'
  },
  devServer: {
    static: {
      directory: path.join(__dirname, 'public/dist'),
    },
    compress: true,
    port: 9000,
  },
  module: {
    rules: [
      {
        test: /\.(jsx|js)$/,
        include: path.resolve(__dirname, 'src'),
        exclude: /node_modules/,
        use: [{
          loader: 'babel-loader',
          options: {
            presets: [
              ['@babel/preset-env', {
                "targets": "defaults" 
              }],
              '@babel/preset-react'
            ]
          }
        }]
      }
    ]
  }
}
