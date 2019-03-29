<template>
    <v-layout align-center column justify-center>
        <v-flex xs12>
            <v-card>
                <Calendar :initialDate="new Date()" @daySelected="daySelected"></Calendar>
            </v-card>
            <CourseList :date="watchingDate" class="mt-3"></CourseList>
        </v-flex>
    </v-layout>
</template>

<script lang="ts">
    import {namespace} from "~/node_modules/vuex-class";
    import {Component, Vue} from "~/node_modules/vue-property-decorator";
    import CourseList from "~/components/schedule/courseList.vue";
    import Calendar from "~/components/schedule/calendar.vue";

    const CourseNamespace = namespace("course");
    @Component({
        components: {CourseList, Calendar}
    })
    export default class Schedule extends Vue {
        watchingDate = new Date();
        @CourseNamespace.Action fetchCourses!: () => void;

        daySelected(theDate: Date) {
            this.watchingDate = theDate as any;
        }
    }
</script>
