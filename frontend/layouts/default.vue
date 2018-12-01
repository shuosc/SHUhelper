<template>
    <v-app dark>
        <v-navigation-drawer
            :mini-variant.sync="miniVariant"
            :clipped="clipped"
            v-model="drawer"
            fixed
            app>
            <v-list>
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
        <v-toolbar fixed app :clipped-left="clipped">
            <v-toolbar-side-icon @click="drawer = !drawer"></v-toolbar-side-icon>
            <v-btn
                icon
                @click.stop="miniVariant = !miniVariant">
                <v-icon v-html="miniVariant ? 'chevron_right' : 'chevron_left'"></v-icon>
            </v-btn>
            <v-btn
                icon
                @click.stop="clipped = !clipped">
                <v-icon>web</v-icon>
            </v-btn>
            <v-btn
                icon
                @click.stop="fixed = !fixed">
                <v-icon>remove</v-icon>
            </v-btn>
            <v-toolbar-title v-text="title"></v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn
                icon
                @click.stop="rightDrawer = !rightDrawer">
                <v-icon>menu</v-icon>
            </v-btn>
        </v-toolbar>
        <v-content>
            <v-container>
                <nuxt/>
            </v-container>
        </v-content>
        <v-navigation-drawer
            temporary
            :right="right"
            v-model="rightDrawer"
            fixed>
            <v-list>
                <v-list-tile @click.native="right = !right">
                    <v-list-tile-action>
                        <v-icon light>compare_arrows</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-title>Switch drawer (click me)</v-list-tile-title>
                </v-list-tile>
            </v-list>
        </v-navigation-drawer>
        <v-footer :fixed="fixed" app>
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

        clipped = false;
        drawer = true;
        fixed = false;
        miniVariant = false;
        right = true;
        rightDrawer = false;
        title = 'Vuetify.js';
        items = [
            { icon: 'apps', title: 'Welcome', to: '/' },
            { icon: 'bubble_chart', title: 'Inspire', to: '/inspire' }
        ];
    };
</script>
