const URL_PREFIX = process.env.URL_PREFIX || '/shuhelper/';
const PROXY_PREFIX = process.env.PROXY_PREFIX || URL_PREFIX;

const AUTH_BACKEND_URL = process.env.AUTH_BACKEND_URL || 'http://localhost:3001';
const API_BACKEND_URL = process.env.API_BACKEND_URL || 'http://localhost:3001';

module.exports = {
    dev: process.env.NODE_ENV !== 'production',
    modules: [
        '~/modules/typescript',
        '@nuxtjs/vuetify',
        '@nuxtjs/axios',
        '@nuxtjs/proxy'
    ],
    plugins: [{
        src: '~/plugins/vueFlatSurfaceShader',
        ssr: false
    }, {
        src: '~/plugins/fetchOnRefresh',
        ssr: true
    }],
    axios: {
        prefix: URL_PREFIX,
        proxy: true,
        credentials: true
    },
    proxy: {
        [PROXY_PREFIX + 'auth']: {
            target: AUTH_BACKEND_URL,
            pathRewrite: {
                [`^${PROXY_PREFIX}auth`]: '/auth'
            }
        },
        [PROXY_PREFIX + 'api']: {
            target: API_BACKEND_URL,
            pathRewrite: {
                [`^${PROXY_PREFIX}api`]: '/api'
            }
        }
    },
    router: {
        base: URL_PREFIX
    },
    vuetify: {
        materialIcons: false
    }
};