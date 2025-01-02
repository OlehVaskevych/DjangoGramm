const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin'); // Підключаємо CleanWebpackPlugin
const { VueLoaderPlugin } = require('vue-loader');

module.exports = {
    entry: './assets/scripts/index.js', // Головний JS файл
    output: {
        path: path.resolve(__dirname, './static/dist/'), // Куди зберігати файли
        filename: 'bundle.js',
        publicPath: '/static/dist/', // URL для Webpack Dev Server
    },
    watch: true, // Відстеження змін у файлах
    mode: 'development',
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env'],
                    },
                },
            },
            {
                test: /\.css$/,
                use: [
                    MiniCssExtractPlugin.loader, // Витягує CSS в окремий файл
                    'css-loader', // Інтерпретує @import та url() у CSS
                ],
            },
            {
                test: /\.(png|jpg|gif|svg)$/,
                type: 'asset/resource',
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader',
            },
        ],
    },
    devServer: {
        static: {
            directory: path.join(__dirname, './static/'),
        },
        compress: true,
        port: 8080,
    },
    plugins: [
        new CleanWebpackPlugin(), // Додаємо плагін для очищення папки dist
        new MiniCssExtractPlugin({
            filename: 'styles.css', // Назва для зібраного CSS-файлу
        }),
        new VueLoaderPlugin(),
    ],
    resolve: {
        alias: {
            vue: 'vue/dist/vue.esm-browser.js'
        },
        extensions: ['.js', '.vue']
    },
};
