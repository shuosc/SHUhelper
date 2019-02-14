<template>
    <v-app dark>
        <v-navigation-drawer :mini-variant="miniVariant" app fixed v-model="drawer">
            <v-list>
                <v-list-tile avatar class="auth-button">
                    <v-list-tile-avatar>
                        <img src="~/assets/image/avatar_default.jpg" alt="">
                    </v-list-tile-avatar>
                    <v-layout align-center fill-height justify-space-between row>
                        <v-list-tile-title>{{this.student.isNull?'游客':this.student.value.name}}</v-list-tile-title>
                        <v-list-tile-sub-title class="auth-button">
                            <v-btn @click="auth" flat small>
                                {{this.student.isNull?'登录':'注销'}}
                            </v-btn>
                        </v-list-tile-sub-title>
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
            <span>&copy; 2017 ~ {{(new Date()).getFullYear() }}</span>
        </v-footer>
    </v-app>
</template>

<script lang="ts">
    import Component, {namespace} from 'nuxt-class-component';
    import Vue from 'vue';
    import * as student from '~/store/modules/student';
    import {Student} from '~/store/modules/student';
    import {Maybe} from "../../shared/tools/functools/maybe";

    const StudentNamespace = namespace(student.name);
    @Component
    export default class extends Vue {
        @StudentNamespace.Getter student!: Maybe<Student>;
        @StudentNamespace.Action doLogout!: () => void;
        drawer = true;
        miniVariant = false;
        title = 'SHUHelper';
        items = [
            {icon: 'school', title: '首页', to: '/'},
            {icon: 'calendar_today', title: '日程', to: '/schedule'}
        ];

        auth() {
            if (this.student.isNull) {
                this.$router.push('/login');
            } else {
                this.doLogout();
                localStorage.clear();
                this.$router.push('/');
                window.location.reload();
            }
        }
    };
</script>

<style>
    .auth-button {
        text-align: right;
    }
</style>