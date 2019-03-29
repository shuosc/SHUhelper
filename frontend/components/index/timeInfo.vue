<template>
    <v-card class="pa-0 mt-2">
        <v-card-title class="pa-0" primary-title>
            <v-container class="pa-3">
                <v-layout align-center row wrap>
                    <v-flex fill-height xs1>
                        <v-layout align-center justify-center>
                            <v-avatar :size="avatarSize() ">
                                <v-icon class="white--text orange lighten-1" medium>class</v-icon>
                            </v-avatar>
                        </v-layout>
                    </v-flex>
                    <v-divider class="mx-3" inset vertical></v-divider>
                    <v-flex xs9>
                        <v-layout row wrap>
                            <v-flex xs12>
                                现在是 {{format(now,"HH点mm分ss秒")}}
                            </v-flex>
                            <v-flex v-if="student.isNone()" xs12>
                                <v-btn @click="$router.push('/login')" block color="primary">需要登录</v-btn>
                            </v-flex>
                            <template v-else-if="currentDateInSemester.isSome()">
                                <v-flex v-if="currentDateInSemester.chain(getHoliday).isSome()" xs12>
                                    今天放假！
                                </v-flex>
                                <v-flex v-else-if="now.getDay() === 0 || now.getDay() === 6" xs12>
                                    今天周末！
                                </v-flex>
                                <v-flex v-else xs12>
                                    <template v-if="currentDateInSemester.map(isBeforeFirstSector).getOrElse(false)">
                                        时间还早，不再睡会？
                                    </template>
                                    <template v-else-if="currentDateInSemester.map(isAfterLastSector).getOrElse(false)">
                                        已经很晚了，不去休息吗？
                                    </template>
                                    <v-layout align-center row
                                              v-else-if="this.currentDateInSemester.chain(currentSector).isSome()" wrap>
                                        <v-flex sm1 xs2>
                                            <v-progress-circular
                                                    :size="30"
                                                    :value="100-currentSectorPassedPercentage.toNullable()"
                                                    :width="2"
                                                    color="red">
                                                {{45 - minutesPassedFromThisSectorBegin.map(Math.round).toNullable()}}
                                            </v-progress-circular>
                                        </v-flex>
                                        <v-flex sm11 xs10>
                                            <v-layout row wrap>
                                                <template v-if="currentClass.isSome()">
                                                    <v-flex md2 sm3 text-sm-right text-xs-right xs12>你应该在上</v-flex>
                                                    <v-flex md10 sm9 text-sm-left text-xs-right xs12>
                                                        {{currentClass.chain(it => course(it.courseId)).chain(it =>
                                                        it.name)}}
                                                    </v-flex>
                                                </template>
                                                <v-flex text-sm-left text-xs-right v-else xs12>
                                                    这节你好像没课😊
                                                </v-flex>
                                            </v-layout>
                                        </v-flex>
                                    </v-layout>
                                    <v-layout align-center row v-else wrap>
                                        <v-flex sm1 xs2>
                                            <v-progress-circular
                                                    :size="30"
                                                    :value="100-currentRestPassedPercentage.toNullable()"
                                                    :width="2"
                                                    color="green">
                                                {{restRestMinutes.toNullable()}}
                                            </v-progress-circular>
                                        </v-flex>
                                        <v-flex sm11 xs10>
                                            <v-layout row wrap>
                                                <v-flex text-sm-left text-xs-right xs12>
                                                    下节课还有 {{restRestMinutes.toNullable()}} 分钟上课
                                                </v-flex>
                                                <template v-if="nextClass.isSome()">
                                                    <v-flex md3 sm4 text-sm-left text-xs-right xs12>你下节课要上的是</v-flex>
                                                    <v-flex md9 sm8 text-sm-left text-xs-right xs12>
                                                        {{course(nextClass.toNullable().courseId).toNullable().name}}
                                                    </v-flex>
                                                </template>
                                                <v-flex sm8 text-sm-left text-xs-right v-else xs12>然而你下节课好像没课😊</v-flex>
                                            </v-layout>
                                        </v-flex>
                                    </v-layout>
                                </v-flex>
                            </template>
                        </v-layout>
                    </v-flex>
                </v-layout>
            </v-container>
        </v-card-title>
    </v-card>
</template>

<script lang="ts">
    import {avatarSize} from "~/tools/avatarSize";
    import {DateTimeInSemester, DateTimeInSemesterService} from "~/service/dateTimeInSemester.service";
    import {Component, Vue} from "~/node_modules/vue-property-decorator";
    import {namespace} from "~/node_modules/vuex-class";
    import {option, Option, some} from "~/node_modules/fp-ts/lib/Option";
    import {Semester} from "../../../shared/model/semester/semester";
    import {Student} from "../../../shared/model/student/student";
    import {extractTime} from "~/tools/dateTime";
    import {differenceInMinutes, format} from "date-fns";
    import {Class} from "../../../shared/model/course/class/class";
    import {liftA2} from "~/node_modules/fp-ts/lib/Apply";
    import {curry, flip} from "~/node_modules/fp-ts/lib/function";
    import {findFirst} from "~/node_modules/fp-ts/lib/Array";
    import {SectorService} from "~/service/sector.service";
    import {ClassService} from "~/service/class.service";
    import {toPercent} from "~/tools/toPercent";
    import {Course} from "../../../shared/model/course/course";
    import isAfterLastSector = DateTimeInSemesterService.isAfterLastSector;
    import currentSector = DateTimeInSemesterService.currentSector;
    import isBeforeFirstSector = DateTimeInSemesterService.isBeforeFirstSector;
    import getHoliday = DateTimeInSemesterService.getHoliday;

    const StudentNamespace = namespace("student");
    const SemesterNamespace = namespace("semester");
    const CourseNamespace = namespace("course");


    @Component({
        methods: {
            avatarSize,
            getHoliday,
            isBeforeFirstSector,
            isAfterLastSector,
            currentSector,
            format
        }
    })
    export default class TimeInfo extends Vue {
        @SemesterNamespace.Getter semesterForDate!: (date: Date) => Option<Semester>;
        @SemesterNamespace.Action fetchCurrent!: () => void;
        @StudentNamespace.Getter student!: Option<Student>;
        @CourseNamespace.Getter classesForDate!: (dateInSemester: DateTimeInSemester) => Array<Class>;
        @CourseNamespace.Getter course!: (id: any) => Option<Course>;
        @CourseNamespace.Action fetchCourses!: () => void;
        now = new Date();

        async mounted() {
            await this.fetchCurrent();
            await this.fetchCourses();
            setInterval(() => {
                this.now = new Date();
            }, 1000);
        }

        get current() {
            if (this.semesterForDate(this.now).isNone()) {
                this.fetchCurrent();
            }
            return this.semesterForDate(this.now);
        }

        get currentDateInSemester(): Option<DateTimeInSemester> {
            return this.current.map(current => {
                return {
                    semester: current,
                    dateTime: this.now as any
                }
            });
        }

        get minutesPassedFromThisSectorBegin() {
            return this.currentDateInSemester.chain(currentSector)
                .map(it => differenceInMinutes(extractTime(this.now), it.start));
        }

        get currentSectorPassedPercentage() {
            return this.minutesPassedFromThisSectorBegin
                .map(it => it * 100 / 45)
                .map(Math.round);
        }

        get currentClass(): Option<Class> {
            const isOnDateTime = (it: Class): boolean => liftA2(option)(curry(ClassService.isOnDateTime))(some(it))(this.currentDateInSemester).getOrElse(false);
            return this.currentDateInSemester
                .map(this.classesForDate)
                .chain(it => findFirst(it, isOnDateTime));
        }

        get nextClass(): Option<Class> {
            const restIndex = SectorService.restIndexForTime(this.now);
            const nextSectorIndex: Option<number> = restIndex.map(it => it + 1);
            const isNextClass = nextSectorIndex
                .map(flip(curry(ClassService.isOnSector)))
                .getOrElse((class_: Class) => false);
            return this.currentDateInSemester
                .map(this.classesForDate)
                .chain(it => findFirst(it, isNextClass));
        }

        get currentRest(): Option<Interval> {
            return this.currentDateInSemester.chain(DateTimeInSemesterService.currentRest);
        }

        get currentRestMinutes(): Option<number> {
            return this.currentRest.map(it => differenceInMinutes(it.end, it.start));
        }

        get currentRestPassedMinutes(): Option<number> {
            return this.currentRest.map(it => differenceInMinutes(extractTime(this.now), it.start));
        }

        get restRestMinutes(): Option<number> {
            return liftA2(option)(curry((a: number, b: number) => a - b))(this.currentRestMinutes)(this.currentRestPassedMinutes);
        }

        get currentRestPassedPercentage(): Option<number> {
            return liftA2(option)(curry(toPercent))(this.currentRestPassedMinutes)(this.currentRestMinutes);
        }
    }
</script>
