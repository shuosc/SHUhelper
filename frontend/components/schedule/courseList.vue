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
    import * as semesters from '~/store/modules/semester';
    import {Maybe} from "../../../shared/tools/functools/maybe";
    import {Semester} from "../../../shared/model/semester/semester";
    import * as _ from "lodash";

    const Courses = namespace(courses.name);
    const Semesters = namespace(semesters.name);
    @Component
    export default class CourseList extends Vue {
        @Prop({default: null})
        date!: Date;

        @Courses.Getter getClassesForDate: any;
        @Courses.Getter getCourse: any;
        @Semesters.Getter getSemesterForDate: any;

        private getTimeForDate(course: Course, date: Date): Class {
            return course.classes.filter((time: Class) => {
                return time.day === date.getDay();
            })[0];
        }

        get allCourses(): Array<Course> {
            if (this.date === null) {
                return [];
            }
            const semester: Maybe<Semester> = this.getSemesterForDate(this.date);
            const getClassesForToday: (semester: Semester) => Array<Class> = _.partial(this.getClassesForDate, _, this.date);
            const classesForDate: Maybe<Array<Class>> = semester.map(getClassesForToday);
            if (classesForDate.value === null) {
                return [];
            }
            const classTimeComp = (classA: Class, classB: Class) => classA.beginSector - classB.beginSector;
            const classes = classesForDate.value.sort(classTimeComp);
            const getCoursesForClasses = (classes: Array<Class>): Array<Maybe<Course>> => classes.map(class_ => this.getCourse(class_.courseId));
            return getCoursesForClasses(classes).map(it => it.value) as any as Course[];
        }
    }
</script>

<style scoped>
    .class-info {
        padding: 0;
    }
</style>