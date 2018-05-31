const path = require('path')
const webpack = require('webpack')
const FriendlyErrorsPlugin = require('friendly-errors-webpack-plugin')
const CompressionPlugin = require('compression-webpack-plugin')
const ExtractTextPlugin = require('extract-text-webpack-plugin')
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin')
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
const CssNano = require('cssnano')
// const HtmlWebpackPlugin = require('html-webpack-plugin')
// const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin

module.exports = {
  entry: './src/main.js',
  output: {
    path: path.resolve(__dirname, './dist'),
    publicPath: '/dist/',
    filename: 'bundle.js'
    // filename: '[name].[chunkhash].js',
  },
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: [
            {
              loader: 'css-loader!sass-loader',
              options: {
                minimize: true,
                sourceMap: false
              }
            }
          ]
        }),
        exclude: /node_modules/
      },
      {
        test: /\.sass$/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: [
            {
              loader: 'sass-loader?indentedSyntax=1r',
              options: {
                minimize: true,
                sourceMap: false
              }
            }
          ]
        }),
        exclude: /node_modules/
      },
      {
        test: /\.css$/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: [
            {
              loader: 'css-loader',
              options: {
                minimize: true,
                sourceMap: false
              }
            }
          ]
        })
      },
      {
        enforce: 'pre',
        test: /\.(ya?ml|json)$/,
        use: {
          loader: 'yaml-import-loader',
          options: {
            importRoot: true,
            importNested: true,
            importKeyword: 'import',
            importRawKeyword: 'import-raw',
            output: 'object',
            parser: {
              types: [],
              schema: require('js-yaml').SAFE_SCHEMA,
              allowDuplicate: true,
              onWarning: undefined
            }
          }
        }
      },
      {
        test: /\.(json|yaml|yml)$/i,
        loader: '@kazupon/vue-i18n-loader',
        include: '/src/i18n'
      },
      {
        test: /\.(woff2?|ttf|eot)(\?v=\d+\.\d+\.\d+)?$/,
        loader: 'url-loader?limit=10000'
      },
      {
        // Lint local *.vue files
        enforce: 'pre',
        test: /\.vue$/,
        loader: 'eslint-loader',
        exclude: /node_modules/,
        options: {
          fix: true
        }
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          preLoaders: {
            i18n: 'yaml-loader'
          },
          loaders: {
            i18n: '@kazupon/vue-i18n-loader',
            scss: 'vue-style-loader!css-loader!sass-loader',
            sass: 'vue-style-loader!css-loader!sass-loader?indentedSyntax=1&data=@import "./src/assets/sass/main.sass"'
          }
          // other vue-loader options go here
        }
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        loader: 'file-loader',
        options: {
          name: '[name].[ext]?[hash]'
        }
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.vue', '.json', '.css', 'scss'],
    alias: {
      'vue$': 'vue/dist/vue.esm.js'
    }
  },
  devServer: {
    historyApiFallback: true,
    noInfo: true,
    quiet: true // Off, Using FriendlyErrorsPlugin
  },
  performance: {
    hints: false
  },
  // devtool: '#eval-source-map',
  devtool: '#eval-cheap-module-source-map',
  plugins: [
    new FriendlyErrorsPlugin(),
    new ExtractTextPlugin('bundle.css'),
    new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/)
  ]
}

if (process.env.NODE_ENV === 'production') {
  module.exports.devtool = '#source-map'
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true
    }),
    new webpack.optimize.CommonsChunkPlugin({
      children: true,
      async: true
    }),
    new UglifyJsPlugin({
      sourceMap: false,
      mangle:    true,
      compress: {
        pure_getters  : true,
        sequences     : true,
        booleans      : true,
        loops         : true,
        unused        : true,
        warnings      : false,
        drop_console  : true,
        unsafe        : true,
        unsafe_comps  : true,
        screw_ie8     : true
      },
      include: /\.min\.js$/
    }),
    new OptimizeCssAssetsPlugin({
      assetNameRegExp: /\.min\.css$/g,
      cssProcessor: CssNano,
      cssProcessorOptions: { discardComments: { removeAll: true } },
      canPrint: true
    }),
    new CompressionPlugin({
      include: /\.(js|css|woff2?|ttf|eot|svg)/,
      algorithm: 'gzip',
      minRatio: 0.5,
      cache: true
    })
    /*
    new HtmlWebpackPlugin({
      filename: 'index.html',
      template: 'index.html',
      inject:   true,
      chunksSortMode: 'dependency'
    })
    */
  ])
} else {
  /*
  module.exports.plugins = (module.exports.plugins || []).concat([
    new BundleAnalyzerPlugin()
  ])
  */
}
