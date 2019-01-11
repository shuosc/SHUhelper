module.exports = {
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
    plugins: [
        {
            src: '~/plugins/vueFlatSurfaceShader',
            ssr: false
        },
        {
            src: '~/plugins/fetchOnRefresh',
            ssr: true
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