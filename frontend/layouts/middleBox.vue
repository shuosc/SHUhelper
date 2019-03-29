<template>
    <div class="app">
        <no-ssr>
            <flat-surface-shader class="shader" type="webgl"
                                 :light="{ambient: '#22bc9e', diffuse: '#2b7c6b'}"/>
        </no-ssr>
        <div class="mask"></div>
        <v-app>
            <v-content>
                <v-container fluid fill-height>
                    <v-layout align-center justify-center>
                        <v-flex xs8 sm6 md4 class="content">
                            <nuxt/>
                        </v-flex>
                    </v-layout>
                </v-container>
            </v-content>
        </v-app>
    </div>
</template>

<script lang="ts">

    import {Component, Vue} from "vue-property-decorator";

    @Component
    export default class MiddleBox extends Vue {
    };
</script>

<style scoped>
    .mask,
    .shader {
        width: 100vw;
        height: 100vh;
        position: absolute;
        top: 0;
        left: 0;
    }

    .shader {
        z-index: 0;
    }

    .mask {
        background: rgba(0, 0, 0, 0.6);
        z-index: 1;
    }

    .content {
        z-index: 2;
    }
</style>