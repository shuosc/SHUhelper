<template>
    <div>
        <DateInfo class="mt-3"></DateInfo>
        <CourseInfo class="mt-3"></CourseInfo>
    </div>
</template>

<script lang="ts">
    import Component from 'nuxt-class-component';
    import Vue from 'vue';
    import DateInfo from "~/components/index/dateInfo.vue";
    import CourseInfo from "~/components/index/courseInfo.vue";

    @Component({
        components: {
            DateInfo,
            CourseInfo
        }
    })
    export default class Index extends Vue {
        async fetch(context: { store: any, params: any }) {
            // vuex is a piece of sh*t!
            // use plain string? serious?
            await context.store.dispatch("semester/fetchCurrentSemester");
            await context.store.dispatch("course/fetchCourses");
        }
    }
</script>

<style scoped>

</style>