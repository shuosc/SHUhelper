<template>
    <v-app dark>
        <v-navigation-drawer :mini-variant.sync="miniVariant" app fixed v-model="drawer">
            <v-list>
                <v-list-tile v-if="token === ''">
                    <v-btn block color="primary" nuxt to="/admin/login">输入token</v-btn>
                </v-list-tile>
                <v-list-tile v-else>
                    token已经输入
                </v-list-tile>
                <v-list-tile
                        :key="i"
                        :to="item.to"
                        exact
                        router
                        v-for="(item, i) in items">
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
                    @click.stop="miniVariant = !miniVariant"
                    icon>
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
            <span>&copy; 2017 ~ {{(new Date()).getFullYear() }}</span>
        </v-footer>
    </v-app>
</template>

<script lang="ts">
    import Component, {namespace} from 'nuxt-class-component';
    import Vue from 'vue';
    import * as adminModule from '~/store/modules/admin';

    const AdminNamespace = namespace(adminModule.name);

    @Component
    export default class extends Vue {
        @AdminNamespace.Getter token!: string;

        drawer = true;
        miniVariant = false;
        title = 'SHUHelper Admin';
        items = [
            {icon: 'calendar_today', title: '学期', to: '/admin/semester'}
        ];

        mounted() {
            if (this.token === "") {
                this.$router.push("/admin/login")
            }
        }
    };
</script>

<style>
</style>