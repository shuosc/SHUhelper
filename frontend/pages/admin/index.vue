<template>
    <h1>
        在左侧选择功能
    </h1>
</template>

<script lang="ts">
    import Component from 'nuxt-class-component';
    import Vue from 'vue';

    @Component
    export default class Admin extends Vue {
        token = "";

        layout() {
            return "admin"
        }

        submit() {

        }
    }
</script>

<style scoped>

</style>