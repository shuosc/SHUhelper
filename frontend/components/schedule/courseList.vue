<template>
    <v-card>
        <v-list-tile
                :key="course.name"
                @click=""
                avatar
                v-for="course in allCourses"
        >
            <v-list-tile-avatar>
                <v-icon>class</v-icon>
            </v-list-tile-avatar>

            <v-list-tile-content>
                <v-list-tile-title>{{ course.name }}</v-list-tile-title>
                <v-list-tile-sub-title>{{ getTimeForDate(course,date).beginSector }}-{{
                    getTimeForDate(course,date).endSector }}
                </v-list-tile-sub-title>
            </v-list-tile-content>

            <v-list-tile-action>
                <v-btn icon ripple>
                    <v-icon color="grey lighten-1">info</v-icon>
                </v-btn>
            </v-list-tile-action>
        </v-list-tile>
    </v-card>
</template>

<script lang="ts">
    import Component from 'nuxt-class-component';
    import {Prop, Vue} from 'vue-property-decorator';
    import {Course} from "~/store/modules/course";
    import {CourseTime} from "../../../shared/model/courseTime/courseTime";

    @Component
    export default class CourseList extends Vue {
        @Prop({default: []})
        courses!: Array<Course>;

        @Prop({default: null})
        date!: Date;

        private getTimeForDate(course: Course, date: Date): CourseTime {
            return course.time.filter((time: CourseTime) => {
                return time.day === date.getDay();
            })[0];
        }

        get allCourses() {
            return this.courses.sort((a: Course, b: Course) => {
                return this.getTimeForDate(a, this.date).beginSector - this.getTimeForDate(b, this.date).endSector;
            })
        }
    }
</script>

<style scoped>

</style>