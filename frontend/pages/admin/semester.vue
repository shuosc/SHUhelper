<template>
    <v-card>
        <v-expansion-panel class="purple">
            <v-expansion-panel-content
                    :key="semester.name"
                    v-for="semester in semesters"
            >
                <div slot="header">{{semester.name}}</div>
                <SemesterEditor :data="semester"></SemesterEditor>
            </v-expansion-panel-content>
        </v-expansion-panel>
        <v-flex xs12>
            <v-btn @click="addSemester" block color="primary mt-0">添加学期</v-btn>
        </v-flex>
    </v-card>
</template>

<script lang="ts">
    import Component, {namespace} from 'nuxt-class-component';
    import {Vue} from 'vue-property-decorator';
    import * as semesterModule from '~/store/modules/semester';
    import SemesterEditor from "~/components/admin/semesterEditor.vue";

    const SemesterNamespace = namespace(semesterModule.name);
    @Component({
        components: {SemesterEditor}
    })
    export default class Semester extends Vue {
        @SemesterNamespace.Getter semesters!: Array<Semester>;
        @SemesterNamespace.Action postSemester!: () => void;

        layout() {
            return "admin"
        }

        async fetch(context: { store: any, params: any }) {
            await context.store.dispatch("semester/fetchAllSemester");
        }

        addSemester() {
            this.postSemester();
        }
    }
</script>

<style scoped>

</style>