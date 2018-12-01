<template>
    <v-app>
        <v-content fill-height>
            <nuxt/>
        </v-content>
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
    };
</script>

<style>
</style>
