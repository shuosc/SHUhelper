<template>
    <v-app dark>
        <v-navigation-drawer :mini-variant.sync="miniVariant" app fixed v-model="drawer">
            <v-list>
                <v-list-tile :to="'sign-in'" avatar class="login">
                    <v-list-tile-avatar>
                        <img :src="avatar" alt="">
                    </v-list-tile-avatar>
                    <v-layout align-center fill-height justify-space-between row>
                        <v-list-tile-title>游客</v-list-tile-title>
                        <v-list-tile-sub-title>登录</v-list-tile-sub-title>
                    </v-layout>
                </v-list-tile>
                <v-list-tile
                    router
                    :to="item.to"
                    :key="i"
                    v-for="(item, i) in items"
                    exact>
                    <v-list-tile-action>
                        <v-icon v-html="item.icon"></v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title v-text="item.title"></v-list-tile-title>
                    </v-list-tile-content>
                </v-list-tile>
            </v-list>
        </v-navigation-drawer>
        <v-toolbar app fixed>
            <v-toolbar-side-icon @click="drawer = !drawer"></v-toolbar-side-icon>
            <v-btn
                icon
                @click.stop="miniVariant = !miniVariant">
                <v-icon v-html="miniVariant ? 'chevron_right' : 'chevron_left'"></v-icon>
            </v-btn>
            <v-toolbar-title v-text="title"></v-toolbar-title>
            <v-spacer></v-spacer>
        </v-toolbar>
        <v-content>
            <v-container>
                <nuxt/>
            </v-container>
        </v-content>
        <v-footer app>
            <span>&copy; 2017</span>
        </v-footer>
    </v-app>
</template>

<script lang="ts">
    import Component from 'nuxt-class-component';
    import Vue from 'vue';
    import { namespace, State } from 'vuex-class';

    import * as auth from '../store/modules/auth';

    const AuthState = namespace(auth.name, State);

    @Component
    export default class extends Vue {
        @AuthState isLogged: boolean;
        drawer = true;
        miniVariant = false;
        title = 'SHUHelper';
        items = [
            { icon: 'school', title: '首页', to: '/' },
            { icon: 'explore', title: '应用', to: '/apps' },
            { icon: 'filter_vintage', title: '广场', to: '/square' },
            { icon: 'calendar_today', title: '日程', to: '/schedule' },
            { icon: 'info', title: '关于', to: '/about' }
        ];
        avatar = require('~/assets/images/avatar_default.jpg');
    };
</script>

<style lang="stylus">
    .login {
        margin 10px

        a {
            border-radius 6px
        }

        .list__tile__title {
            width auto
        }

        .list__tile__sub-title {
            width auto
        }
    }

    .navigation-drawer.navigation-drawer--mini-variant {
        .list__tile.list__tile--link.list__tile--avatar {
            padding-left 5px
        }
    }
</style>
