const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  publicPath: './',
  transpileDependencies: [
    'vuetify'
  ],
  pluginOptions: {
    electronBuilder:{
      builderOptions: {
        files: [
          "**/*"
        ],
        extraFiles:[
          {
          "from": "src/server",
          "to": "src/server",
          "filter":["**/*"]
        },
          {
          "from": "venv",
          "to": "venv",
          "filter":["**/*"]
        }
      ]

      }

    }
  }
})
