<template>
    <div>
        <DateInfo></DateInfo>
        <TimeInfo></TimeInfo>
        <BusTimeInfo></BusTimeInfo>
    </div>
</template>

<script lang="ts">
    import {Component, Vue} from "vue-property-decorator";
    import DateInfo from "~/components/index/dateInfo.vue";
    import TimeInfo from "~/components/index/timeInfo.vue";
    import BusTimeInfo from "~/components/index/busTimeInfo.vue";

    @Component({
        components: {BusTimeInfo, TimeInfo, DateInfo}
    })
    export default class Index extends Vue {
    }
</script>

<style>
    .auth-button {
        text-align: right;
    }
</style>
