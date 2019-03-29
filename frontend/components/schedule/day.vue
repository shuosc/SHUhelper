<template>
    <v-flex :class="{today: isToday,'non-empty': date.isSome()}" @click="clicked" class="day">
        <v-container align-center fill-height justify-center>
            <v-layout column>
                <v-flex class="date-number-wrapper text-xs-center">
                    <span class="date-number">{{date.map(it => it.getDate()).getOrElse('')}}</span>
                </v-flex>
                <v-flex class="dots text-xs-center">
                    <v-layout align-center justify-center row v-if="!isHoliday" wrap>
                        <span :style="{background:course.color}" class="dot"
                              v-for="course in allCourses"></span>
                    </v-layout>
                    <span v-else>
                    假期
                    </span>
                </v-flex>
            </v-layout>
        </v-container>
    </v-flex>
</template>

<script lang="ts">

    import {namespace} from "~/node_modules/vuex-class";
    import {Component, Prop, Vue} from "~/node_modules/vue-property-decorator";
    import {none, Option} from "~/node_modules/fp-ts/lib/Option";
    import {Semester} from "../../../shared/model/semester/semester";
    import {Course} from "~/store/modules/course";
    import {Class} from "../../../shared/model/course/class/class";
    import {DateTimeInSemester, DateTimeInSemesterService} from "~/service/dateTimeInSemester.service";
    import {isSameDay} from "date-fns";

    const SemesterNamespace = namespace("semester");
    const CourseNamespace = namespace("course");

    @Component
    export default class Day extends Vue {
        @Prop({default: () => none})
        date!: Option<Date>;
        @SemesterNamespace.Getter semesterForDate!: (date: Date) => Option<Semester>;
        @SemesterNamespace.Action fetchSemester!: (payload: { forDate: Date }) => void;
        @CourseNamespace.Getter course!: (id: any) => Option<Course>;
        @CourseNamespace.Action fetchCourses!: () => void;
        @CourseNamespace.Getter classesForDate!: (dateInSemester: DateTimeInSemester) => Array<Class>;
        @CourseNamespace.Getter courses!: () => Array<Class>;

        async mounted() {
            if (this.date.isSome())
                await this.fetchSemester({forDate: this.date.toNullable()});
        }

        get semester() {
            return this.date.chain(this.semesterForDate);
        }

        get currentDateInSemester(): Option<DateTimeInSemester> {
            return this.semester.map(semester => {
                return {
                    semester: semester,
                    dateTime: this.date.toNullable() as any
                }
            });
        }

        get isToday(): boolean {
            return this.date.map(it => isSameDay(new Date(), it)).getOrElse(false);
        }

        clicked() {
            if (this.date !== null)
                this.$emit('click', this.date.toNullable());
        }


        get isHoliday() {
            return this.currentDateInSemester.map(DateTimeInSemesterService.isHoliday).getOrElse(false);
        }

        get allCourses(): Array<Course> {
            return this.currentDateInSemester
                .map(this.classesForDate)
                .getOrElse([])
                .map(it => this.course(it.courseId).toNullable());
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

    .day.non-empty:hover {
        cursor pointer;
        background rgba(0, 0, 0, 0.3);

        &.today {
            color #666666
            background #7b8dbf
        }
    }
</style>
