const { override, fixBabelImports, addLessLoader, addWebpackPlugin } = require('customize-cra');
const webpack = require('webpack')
const config = require('./config')

module.exports = override(
  // 按需加载 antd
  fixBabelImports('import', {
    libraryName: 'antd',
    libraryDirectory: 'es',
    style: true,
  }),
  // 添加加载 less 的 javascriptEnabled 和 antd 的主题配置。
  addLessLoader({
    javascriptEnabled: true,
    modifyVars: { '@primary-color': '#1DA57A' },
  }),
  addWebpackPlugin(
    new webpack.DefinePlugin({
      REACT_APP_CONFIG: JSON.stringify(config)
    })
  )
);
