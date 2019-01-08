module.exports = {
    server: {
        port: 8000,
        host: '0.0.0.0',
    },
    dev: process.env.NODE_ENV !== 'production',
    env: {
        baseUrl: process.env.BASE_URL || 'http://localhost:3001'
    },
    modules: [
        '~/modules/typescript',
        '@nuxtjs/vuetify',
        '@nuxtjs/axios',
        '@nuxtjs/proxy'
    ],
    plugins: [{
        src: '~/plugins/vue-flat-surface-shader',
        ssr: false
    }],
    axios: {
        proxy: true,
        credentials: true
    },
    proxy: {
        '/auth': process.env.AUTH_BACKEND_URL || 'http://localhost:3001',
        '/api': process.env.API_BACKEND_URL || 'http://localhost:3001'
    },
};