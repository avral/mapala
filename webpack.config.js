var path = require('path')
var webpack = require('webpack')
var ModernizrWebpackPlugin = require('modernizr-webpack-plugin');

var backEndDomain = process.env.BACK_END_DOMAIN || 'http://127.0.0.1:8000/'
console.log(process.env.NODE_ENV)

var configM = {
  'feature-detects': [
    'input',
    'canvas',
    'css/resize'
  ]
}

module.exports = {
  entry: ['babel-polyfill', './frontend/main.js'],
  output: {
    path: path.resolve(__dirname, 'static'),
    publicPath: '/static/',
    filename: 'build.js'
  },
	plugins: [
		new webpack.ProvidePlugin({
				$: "jquery",
				jQuery: "jquery"
		}),
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'development')
    }),
    new ModernizrWebpackPlugin(configM)
	],
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          loaders: {
          }
          // other vue-loader options go here
        }
      },
			{
				test: /\.css$/,
				use: [ 'style-loader', 'css-loader' ]
			},
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      },
      {
        test: /\.(png|jpg|gif|svg|ttf|woff|woff2|eot)$/,
        loader: 'file-loader',
        options: {
          name: '[name].[ext]?[hash]'
        }
      },
    ],
    loaders: [
      { test: /[\\\/]bower_components[\\\/]modernizr[\\\/]modernizr\.js$/,
            loader: "imports?this=>window!exports?window.Modernizr" }
    ]
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
			'jquery-ui': 'jquery-ui/ui',
			'jquery-ui-css': 'jquery-ui/../../themes/base',
    }
	},
  devServer: {
    historyApiFallback: true,
    noInfo: true,
		proxy: {
      '*': backEndDomain,
		}
  },
  performance: {
    hints: false
  },
  devtool: '#eval-source-map',
  node: {
    fs: 'empty'
  }
}

if (process.env.NODE_ENV === 'production') {
  module.exports.devtool = '#source-map'
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: true,
      compress: {
        warnings: false
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true
    })
  ])
}
