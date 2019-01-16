<template>
    <v-card>
        <v-list-tile
                :key="course.name"
                @click=""
                avatar
                v-for="course in allCourses"
        >
            <v-list-tile-avatar>
                <v-icon :style="{background: course.color}">class</v-icon>
            </v-list-tile-avatar>

            <v-list-tile-content>
                <v-list-tile-title>{{ course.name }}</v-list-tile-title>
                <v-list-tile-sub-title>
                    <v-container class="class-info" grid-list-xs text-xs-left>
                        <v-layout row wrap>
                            <v-flex xs2>{{ getTimeForDate(course,date).beginSector }}-{{
                                getTimeForDate(course,date).endSector }}
                            </v-flex>
                            <v-flex xs10>
                                {{course.place}}
                            </v-flex>
                        </v-layout>
                    </v-container>
                </v-list-tile-sub-title>
            </v-list-tile-content>
        </v-list-tile>
    </v-card>
</template>

<script lang="ts">
    import Component, {namespace} from 'nuxt-class-component';
    import {Prop, Vue} from 'vue-property-decorator';
    import {Class} from "../../../shared/model/course/class/class";
    import {Course} from "../../../shared/model/course/course";
    import * as courses from '~/store/modules/course';

    const Courses = namespace(courses.name);
    @Component
    export default class CourseList extends Vue {
        @Prop({default: null})
        date!: Date;

        @Courses.Getter getCoursesForDate: any;

        private getTimeForDate(course: Course, date: Date): Class {
            return course.classes.filter((time: Class) => {
                return time.day === date.getDay();
            })[0];
        }

        get allCourses() {
            const coursesForDate = this.getCoursesForDate(this.date);
            return coursesForDate.sort((a: Course, b: Course) => {
                return this.getTimeForDate(a, this.date).beginSector - this.getTimeForDate(b, this.date).endSector;
            })
        }
    }
</script>

<style scoped>
    .class-info {
        padding: 0;
    }
</style>