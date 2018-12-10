<template>
    <v-layout column justify-center align-center>
        <v-flex xs12 sm8 md6>
            <v-card>{{$store.state.date}}</v-card>
        </v-flex>
    </v-layout>
</template>

<script lang="ts">
    import Component from 'nuxt-class-component';
    import Vue from 'vue';
    import Axios from 'axios';
    import * as Date from '../store/modules/date';

    @Component
    export default class Index extends Vue {
        async fetch({ store, params }: { store: any, params: any }) {
            let { data } = await Axios.get('https://www.shuhelper.cn/api/time/');
            store.commit(Date.name + '/' + Date.Types.DATE_SET, data);
        }
    }
</script>
