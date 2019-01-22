<template>
    <v-flex :class="{today: isToday,'non-empty': date!=null}" @click="clicked" class="day">
        <v-container align-center fill-height justify-center>
            <v-layout column>
                <v-flex class="date-number-wrapper text-xs-center">
                    <span class="date-number">{{date === null ? '' : date.getDate()}}</span>
                </v-flex>
                <v-flex class="dots text-xs-center">
                    <template v-if="!isHoliday(date)">
                        <v-layout align-center justify-center row wrap>
                        <span :style="{background:course.color}" class="dot"
                              v-for="course in allCourses"></span>
                        </v-layout>
                    </template>
                    <span v-else>
                        假期
                    </span>
                </v-flex>
            </v-layout>
        </v-container>
    </v-flex>
</template>

<script lang="ts">
    import Component, {namespace} from 'nuxt-class-component';
    import Vue from 'vue';
    import {Prop} from 'vue-property-decorator';
    import * as courses from '~/store/modules/course';
    import {Course} from '~/store/modules/course';
    import * as semester from '~/store/modules/semester';
    import {Semester, SemesterService} from "../../../shared/model/semester/semester";
    import {DateService} from "../../../shared/tools/date/date";
    import {Class} from "../../../shared/model/course/class/class";
    import {Maybe} from "../../../shared/tools/functools/maybe";
    import * as _ from "lodash";

    const Semester = namespace(semester.name);
    const Courses = namespace(courses.name);

    @Component
    export default class Day extends Vue {
        @Prop({default: null, type: Date})
        date!: Date;
        @Courses.Getter getClassesForDate: any;
        @Courses.Getter getCourse: any;
        @Semester.Getter getSemesterForDate: any;

        get isToday(): boolean {
            if (this.date === null) {
                return false;
            } else {
                const today = new Date();
                return DateService.isSameDate(today, this.date);
            }
        }

        clicked() {
            if (this.date !== null)
                this.$emit('click', this.date);
        }

        isHoliday() {
            const theSemester = this.getSemesterForDate(this.date);
            if (theSemester.value === null) {
                return false;
            }
            return SemesterService.isHoliday(theSemester.value, this.date);
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
    };
</script>

<style scoped lang="stylus">
    .day {
        flex 14.28%;
        font-size 15pt;
        border-radius 4px;
        user-select none;
        max-height 60px
        min-height 33px
        height 10vw

        .container {
            padding 0

            .date-number-wrapper {
                flex 2
                line-height 100%
                height 33%
                display flex
                flex-direction column
                justify-content center
            }

            @media screen and (max-width: 374px) {
                .dots > span {
                    height 8px
                    font-size 8px
                }
            }

            .dots {
                flex 1
                line-height 100%
                height 66%
                font-size 12px

                .dot {
                    min-width 5px
                    min-height 5px
                    border-radius 5px
                    margin-left 1px
                    margin-right 1px
                }
            }
        }

        &.today {
            color #7b8dbf
        }
    }
</style>
