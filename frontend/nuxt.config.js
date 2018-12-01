module.exports = {
  env: {
    baseUrl: process.env.BASE_URL || 'http://localhost:3000'
  },
  head: {
    title: 'nuxt-typescript-starter',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'Nuxt.js project' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons' }
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: false,
  /*
  ** Build configuration
  */
  plugins: [
    '~/plugins/vuetify.ts',
    // '~/plugins/axios',
    '~/plugins/vue-rxjs',
  ],
  css: ['~/assets/styles/app.styl'],
  build: {
    vendor: ['axios', 'vuex-class', 'nuxt-class-component']
  },
  modules: ['~/modules/typescript', '@nuxtjs/pwa'],
  vendor: [
    '~/plugins/vuetify.ts'
  ],
  extractCSS: true
};
