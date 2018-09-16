const path = require('path');
console.log(path.join(__dirname))
module.exports = {
    mode: 'development',
    entry: './frontend/src/index.js',
    output: {
        path: path.resolve(__dirname, './dist'),
        filename: 'bundle.js',
    },
    module: {
        rules: [
            { test: /\.css$/, loader: 'css-loader' },
            {
                test: /(\.js)|(\.jsx)$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/env', '@babel/react']
                        // presets: ['react']
                    }
                }
            }
        ]
    }
}