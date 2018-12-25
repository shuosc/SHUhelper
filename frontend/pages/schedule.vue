<template>
    <v-layout align-center column justify-center>
        <v-flex xs12>
            <v-card>
                <Calendar :initialDate="new Date()"></Calendar>
            </v-card>
            <v-card>

            </v-card>
        </v-flex>
    </v-layout>
</template>

<script lang="ts">
    import Component from 'nuxt-class-component';
    import {Vue} from 'vue-property-decorator';
    import Calendar from '../components/schedule/calendar.vue';

    @Component({
        components: {Calendar}
    })
    export default class Schedule extends Vue {
    }
</script>

<style scoped>

</style>
