<template>
    <div>
        <DateInfo class="mt-3"></DateInfo>
        <CourseInfo class="mt-3"></CourseInfo>
    </div>
</template>

<script lang="ts">
    import Component, {namespace} from 'nuxt-class-component';
    import Vue from 'vue';
    import DateInfo from "~/components/index/dateInfo.vue";
    import CourseInfo from "~/components/index/courseInfo.vue";
    import * as course from '~/store/modules/course';
    import * as semester from '~/store/modules/semester';

    const Course = namespace(course.name);
    const Semester = namespace(semester.name);

    @Component({
        components: {CourseInfo, DateInfo}
    })
    export default class Index extends Vue {
        @Course.Getter getCourses: any;
        @Semester.Getter getSemesterForDate: any;

        async fetch(context: { store: any, params: any }) {
            await context.store.dispatch("semester/fetchCurrentSemester");
            await context.store.dispatch("course/fetchCourses");
        }
    }
</script>

<style scoped>

</style>