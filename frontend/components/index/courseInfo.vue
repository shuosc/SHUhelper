<template>
    <v-card class="pa-0">
        <v-card-title class="pa-0" primary-title>
            <v-container class="pa-3">
                <v-layout align-center row wrap>
                    <v-flex fill-height xs1>
                        <v-layout align-center justify-center>
                            <v-avatar :size="avatarSize">
                                <v-icon class="white--text orange lighten-1" medium>class</v-icon>
                            </v-avatar>
                        </v-layout>
                    </v-flex>
                    <v-divider
                            class="mx-3"
                            inset
                            vertical
                    ></v-divider>
                    <v-flex xs9>
                        <v-layout row wrap>
                            <v-flex xs12>
                                现在是 {{now.getHours()}} 点
                                {{(now.getMinutes() < 10 ? '0' :'') + now.getMinutes()}} 分
                                {{(now.getSeconds() < 10 ? '0' :'') + now.getSeconds()}} 秒
                            </v-flex>
                            <v-flex v-if="!isLogged" xs12>
                                <v-btn @click="auth" block color="primary">需要登录</v-btn>
                            </v-flex>
                            <v-flex v-else-if="inHoliday.value !== null" xs12>
                                今天放假！
                            </v-flex>
                            <v-flex v-else-if="now.getDay() === 0 || now.getDay() === 6" xs12>
                                今天周末！
                            </v-flex>
                            <v-flex v-else xs12>
                                <template v-if="isBeforeFirstSector(now)">时间还早，不再睡会？</template>
                                <template v-else-if="isAfterLastSector(now)">已经很晚了，不去休息吗？</template>
                                <v-layout align-center row v-else-if="isInASector" wrap>
                                    <v-flex sm1 xs2>
                                        <v-progress-circular
                                                :size="30"
                                                :value="(45 - sectorTimePassed.value)*100/45"
                                                :width="2"
                                                color="red">
                                            {{45 - Math.round(sectorTimePassed.value)}}
                                        </v-progress-circular>
                                    </v-flex>
                                    <template v-if="isHavingClass">
                                        <v-flex sm3 text-sm-right xs10>你应该在上</v-flex>
                                        <v-flex sm8 text-sm-left xs12>
                                            {{getCourse(classForCurrentSector.value.courseId).value.name}}
                                        </v-flex>
                                    </template>
                                    <v-flex sm11 v-else xs10>
                                        这节你好像没课😊
                                    </v-flex>
                                </v-layout>
                                <v-layout align-center row v-else wrap>
                                    <v-flex sm1 xs2>
                                        <v-progress-circular
                                                :size="30"
                                                :value="(restTime.value - restTimePassed.value)*100/restTime.value"
                                                :width="2"
                                                color="green">
                                            {{restTime.value - Math.round(restTimePassed.value)}}
                                        </v-progress-circular>
                                    </v-flex>
                                    <v-flex md5 sm11 xs10>下节课还有 {{restTime.value - Math.round(restTimePassed.value)}}
                                        分钟上课
                                    </v-flex>
                                    <template v-if="classForNextSector.value !== null">
                                        <v-flex md3 sm3 text-sm-right xs12>你下节课要上的是</v-flex>
                                        <v-flex md3 sm8 text-sm-left xs12>
                                            {{getCourse(classForNextSector.value.courseId).value.name}}
                                        </v-flex>
                                    </template>
                                    <v-flex sm8 v-else xs12>然而你下节课好像没课😊</v-flex>
                                </v-layout>
                            </v-flex>
                        </v-layout>
                    </v-flex>
                </v-layout>
            </v-container>
        </v-card-title>
    </v-card>
</template>

<script lang="ts">
    import Vue from 'vue';
    import Component, {namespace} from 'nuxt-class-component';
    import * as student from '~/store/modules/student';
    import * as course from '~/store/modules/course';
    import * as semester from '~/store/modules/semester';
    import {Maybe} from "../../../shared/tools/functools/maybe";
    import {Semester} from "../../../shared/model/semester/semester";
    import {Holiday} from "../../../shared/model/semester/holiday/holiday";
    import {DateRangeService} from "../../../shared/model/dateRange/dateRange";
    import {find} from "../../../shared/tools/functools/find";
    import {SectorService} from "../../../shared/model/course/class/sector";
    import {Class, ClassService} from "../../../shared/model/course/class/class";
    import * as _ from "lodash";
    import {TimeService} from "../../../shared/tools/time/time";
    import isTimeInSector = SectorService.isTimeInSector;
    import nextSector = SectorService.nextSector;
    import currentSector = SectorService.currentSector;
    import isBeforeFirstSector = SectorService.isBeforeFirstSector;
    import isAfterLastSector = SectorService.isAfterLastSector;

    const Student = namespace(student.name);
    const Course = namespace(course.name);
    const Semester = namespace(semester.name);
    declare const process: { client: boolean };

    @Component({
        methods: {
            isTimeInSector,
            nextSector,
            currentSector,
            isBeforeFirstSector,
            isAfterLastSector
        }
    })
    export default class CourseInfo extends Vue {
        @Student.Getter isLogged: any;
        @Course.Getter getClassesForDate: any;
        @Course.Getter getCourse: any;
        @Semester.Getter getSemesterForDate: any;

        nowDateBuffer = new Date();

        timer: number | null = null;

        mounted() {
            this.timer = setInterval(() => {
                this.nowDateBuffer = new Date();
            }, 1000);
        }

        beforeDestory() {
            if (this.timer !== null) {
                clearInterval(this.timer);
            }
        }

        get avatarSize(): number {
            if (process.client) {
                return window.innerWidth > 425 ? 60 : 40;
            }
            return 50;
        }

        auth() {
            this.$router.push('/login');
        }

        get now(): Date {
            return this.nowDateBuffer;
        }

        get thisSemester(): Semester {
            return this.getSemesterForDate(this.now).value;
        }

        get nearestHoliday(): Maybe<Holiday> {
            return DateRangeService.nearestToDate(this.thisSemester.holidays, this.now);
        }

        get inHoliday(): Maybe<Holiday> {
            const isNowIn = _.partial(DateRangeService.isDateIn, _, this.now);
            return find(this.thisSemester.holidays, isNowIn);
        }

        get isHavingClass(): boolean {
            return this.classForCurrentSector.value !== null;
        }

        get isInASector(): boolean {
            return currentSector(this.now).value !== null;
        }

        get classForCurrentSector(): Maybe<Class> {
            const classes = this.getClassesForDate(this.thisSemester, this.now);
            const currentSectorId = currentSector(this.now).value;
            if (currentSectorId !== null) {
                const isClassOnSector = (class_: Class) => ClassService.isOnSector(class_, currentSectorId);
                return find(classes, isClassOnSector)
            }
            return new Maybe<Class>(null);
        }

        get classForNextSector(): Maybe<Class> {
            const classes = this.getClassesForDate(this.thisSemester, this.now);
            const nextSectorId = nextSector(this.now).value;
            if (nextSectorId !== null) {
                const isClassOnSector = (class_: Class) => ClassService.isOnSector(class_, nextSectorId);
                return find(classes, isClassOnSector)
            }
            return new Maybe<Class>(null);
        }

        get sectorTimePassed(): Maybe<number> {
            const currentSectorId = currentSector(this.now);
            const startTime = currentSectorId.map(SectorService.getSectorStartTime);
            const timeDistanceFromNow = _.partial(TimeService.timeDistance, this.now, _);
            return startTime.map(timeDistanceFromNow).map(TimeService.timestampDifferenceToMinutes);
        }

        get restTime(): Maybe<number> {
            return nextSector(this.now)
                .map(it => it - 1)
                .flatMap((it: number): Maybe<number> => it === 0 ? new Maybe<number>(null) : new Maybe(it))
                .map(SectorService.minutesBetweenSectors);
        }

        get restTimePassed(): Maybe<number> {
            const lastSectorEndTime = SectorService.nextSector(this.now).map(it => it - 1).map(SectorService.getSectorEndTime);
            const timeFromNow = _.partial(TimeService.timeDistance, this.now, _);
            return lastSectorEndTime.map(timeFromNow).map(TimeService.timestampDifferenceToMinutes);
        }
    }
</script>

<style scoped>

</style>