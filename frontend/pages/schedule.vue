<template>
    <v-layout align-center column justify-center>
        <v-flex xs12>
            <v-card>
                <Calendar :initialDate="new Date()" @daySelected="daySelected"></Calendar>
            </v-card>
            <CourseList :courses="[]" :date="watchingDate"></CourseList>
        </v-flex>
    </v-layout>
</template>

<script lang="ts">
    import Component from 'nuxt-class-component';
    import {Vue} from 'vue-property-decorator';
    import Calendar from '../components/schedule/calendar.vue';
    import CourseList from "~/components/schedule/courseList.vue";

    @Component({
        components: {CourseList, Calendar}
    })
    export default class Schedule extends Vue {
        watchingDate = new Date();

        async fetch(context: { store: any, params: any }) {
            await context.store.dispatch("course/fetchCourses")
        }

        daySelected(theDate: Date) {
            this.watchingDate = theDate;
        }
    }
</script>

<style scoped>

</style>
