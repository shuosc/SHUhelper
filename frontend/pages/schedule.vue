<template>
    <v-layout align-center column justify-center>
        <v-flex xs12>
            <v-card>
                <Calendar :initialDate="new Date()" @daySelected="daySelected"></Calendar>
            </v-card>
            <CourseList :courses="getCoursesForDate(watchingDate)" :date="watchingDate"></CourseList>
        </v-flex>
    </v-layout>
</template>

<script lang="ts">
    import Component, {namespace} from 'nuxt-class-component';
    import {Vue} from 'vue-property-decorator';
    import Calendar from '../components/schedule/calendar.vue';
    import * as courses from '~/store/modules/courses';
    import CourseList from "~/components/schedule/courseList.vue";

    const Courses = namespace(courses.name);
    @Component({
        components: {CourseList, Calendar}
    })
    export default class Schedule extends Vue {
        @Courses.Getter getCoursesForDate: any;
        @Courses.Action fetchCourses: any;

        watchingDate = new Date();

        async asyncData(context: { store: any }) {
            await context.store.dispatch('courses/fetchCourses');
        }

        daySelected(theDate: Date) {
            this.watchingDate = theDate;
        }
    }
</script>

<style scoped>

</style>
