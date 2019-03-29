import NuxtConfiguration from '@nuxt/config'

const URL_PREFIX = process.env.URL_PREFIX || '/shuhelper/';
const PROXY_PREFIX = process.env.PROXY_PREFIX || '/';
const AUTH_BACKEND_URL = process.env.AUTH_BACKEND_URL || 'http://localhost:3001';
const API_BACKEND_URL = process.env.API_BACKEND_URL || 'http://localhost:3001';

const config: NuxtConfiguration = {
    plugins: [{
        src: '~/plugins/vueFlatSurfaceShader',
        ssr: false
    }],
    modules: [
        "@nuxtjs/axios",
        "@nuxtjs/vuetify"
    ],
    axios: {
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
    head: {
        title: "SHUHelper",
        meta: [
            {charset: "utf-8"},
            {
                name: "viewport",
                content:
                    "width=device-width, initial-scale=1"
            }
        ],
        link: [
            {
                rel: "icon",
                type: "image/x-icon",
                href: "/favicon.ico"
            },
            {
                rel: "stylesheet",
                type: "text/css",
                href: "https://fonts.proxy.ustclug.org/css?family=Roboto:300,400,500,700%7CMaterial+Icons"
            }
        ]
    },
};

export default config;
