<template>
    <v-card class="pa-0">
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
                                现在是 {{now.getHours()}} 点
                                {{(now.getMinutes() < 10 ? '0' :'') + now.getMinutes()}} 分
                                {{(now.getSeconds() < 10 ? '0' :'') + now.getSeconds()}} 秒
                            </v-flex>
                            <v-flex v-if="student.isNull" xs12>
                                <v-btn @click="auth" block color="primary">需要登录</v-btn>
                            </v-flex>
                            <template v-else-if="!currentSemester.isNull">
                                <v-flex v-if="!currentHoliday.isNull" xs12>
                                    今天放假！
                                </v-flex>
                                <v-flex v-else-if="now.getDay() === 0 || now.getDay() === 6" xs12>
                                    今天周末！
                                </v-flex>
                                <v-flex v-else xs12>
                                    <template v-if="isBeforeFirstSector(now)">时间还早，不再睡会？</template>
                                    <template v-else-if="isAfterLastSector(now)">已经很晚了，不去休息吗？</template>
                                    <v-layout align-center row v-else-if="isInASector(now)" wrap>
                                        <v-flex sm1 xs2>
                                            <v-progress-circular
                                                    :size="30"
                                                    :value="100-toPercent(currentSectorMinutesPassed.value,45)"
                                                    :width="2"
                                                    color="red">
                                                {{45 - Math.round(currentSectorMinutesPassed.value)}}
                                            </v-progress-circular>
                                        </v-flex>
                                        <v-flex sm11 xs10>
                                            <v-layout row wrap>
                                                <template v-if="!currentClass.isNull">
                                                    <v-flex md2 sm3 text-sm-right text-xs-right xs12>你应该在上</v-flex>
                                                    <v-flex md10 sm9 text-sm-left text-xs-right xs12>
                                                        {{getCourse(currentClass.value.courseId).value.name}}
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
                                                    :value="100-toPercent(currentPassedRestTime.value,currentTotalRestTime.value)"
                                                    :width="2"
                                                    color="green">
                                                {{currentTotalRestTime.value - currentPassedRestTime.value}}
                                            </v-progress-circular>
                                        </v-flex>
                                        <v-flex sm11 xs10>
                                            <v-layout row wrap>
                                                <v-flex text-sm-left text-xs-right xs12>
                                                    下节课还有
                                                    {{currentTotalRestTime.value - currentPassedRestTime.value}}
                                                    分钟上课
                                                </v-flex>
                                                <template v-if="!nextClass.isNull">
                                                    <v-flex md3 sm4 text-sm-left text-xs-right xs12>你下节课要上的是</v-flex>
                                                    <v-flex md9 sm8 text-sm-left text-xs-right xs12>
                                                        {{getCourse(nextClass.value.courseId).value.name}}
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
    import Vue from 'vue';
    import Component, {namespace} from 'nuxt-class-component';
    import {avatarSize} from "~/tools/avatarSize";
    import * as _ from "lodash";
    import * as semesterModule from '~/store/modules/semester';
    import * as studentModule from '~/store/modules/student';
    import {Student} from '~/store/modules/student';
    import * as courseModule from '~/store/modules/course';
    import {Course} from '~/store/modules/course';
    import {Semester} from "../../../shared/model/semester/semester";
    import {just, Maybe} from "../../../shared/tools/functools/maybe";
    import {Holiday, HolidayWithShift} from "../../../shared/model/semester/holiday/holiday";
    import {DateRangeService} from "../../../shared/model/dateRange/dateRange";
    import {find} from "../../../shared/tools/functools/find";
    import {SectorService} from "../../../shared/model/course/class/sector";
    import {TimeService} from "../../../shared/tools/dateTime/time/time";
    import {toPercent} from "~/tools/toPercent";
    import {Class, ClassService} from "../../../shared/model/course/class/class";
    import isBeforeFirstSector = SectorService.isBeforeFirstSector;
    import isAfterLastSector = SectorService.isAfterLastSector;
    import isInASector = SectorService.isInASector;

    const SemesterNamespace = namespace(semesterModule.name);
    const StudentNamespace = namespace(studentModule.name);
    const CourseNamespace = namespace(courseModule.name);

    @Component({
        methods: {
            avatarSize,
            isBeforeFirstSector,
            isAfterLastSector,
            isInASector,
            toPercent
        }
    })
    export default class CourseInfo extends Vue {
        now = new Date();

        @SemesterNamespace.Getter getSemesterForDate!: (date: Date) => Maybe<Semester>;
        @StudentNamespace.Getter student!: Maybe<Student>;
        @CourseNamespace.Getter getClassesForDate!: (semester: Semester, date: Date) => Array<Class>;
        @CourseNamespace.Getter getCourse!: (id: string) => Maybe<Course>;

        mounted() {
            setInterval(() => {
                this.now = new Date();
            }, 1000);
        }

        auth() {
            this.$router.push('/login');
        }

        get currentSemester(): Maybe<Semester> {
            return this.getSemesterForDate(this.now);
        }

        get currentHoliday(): Maybe<Holiday | HolidayWithShift> {
            const nowIn = _.partial(DateRangeService.isDateIn, _, this.now);
            return this.currentSemester.flatMap(it => find(it.holidays, nowIn));
        }

        get currentSectorMinutesPassed(): Maybe<number> {
            const currentSectorId = SectorService.currentSector(this.now);
            // noinspection TypeScriptValidateTypes
            return just(_.curry(TimeService.timeDistance))
                .apply(currentSectorId.map(SectorService.getSectorStartTime))
                .apply(just(this.now))
                .map(TimeService.timestampDifferenceToMinutes);
        }

        get classes(): Array<Class> {
            const semester: Maybe<Semester> = this.getSemesterForDate(this.now);
            // noinspection TypeScriptValidateTypes
            const result = just(_.curry(this.getClassesForDate)).apply(semester).apply(just(this.now));
            return result.isNull ? [] : result.value;
        }

        get currentClass(): Maybe<Class> {
            const currentSectorId = SectorService.currentSector(this.now).value;
            if (currentSectorId === null) {
                return just<Class>(null);
            }
            return find(this.classes, (class_) => ClassService.isOnSector(class_, currentSectorId));
        }

        get nextClass(): Maybe<Class> {
            const nextSectorId = SectorService.nextSector(this.now).value;
            if (nextSectorId === null) {
                return just<Class>(null);
            }
            return find(this.classes, (class_) => ClassService.isOnSector(class_, nextSectorId));
        }

        get currentTotalRestTime(): Maybe<number> {
            return SectorService.lastSector(this.now).map(SectorService.restTimeAfterSector);
        }

        get currentPassedRestTime(): Maybe<number> {
            const lastSectorEndTime = SectorService.lastSector(this.now).map(SectorService.getSectorEndTime);
            const timeDistanceToNow = _.partial(TimeService.timeDistance, _, this.now);
            return lastSectorEndTime
                .map(timeDistanceToNow)
                .map(TimeService.timestampDifferenceToMinutes);
        }
    }
</script>

<style scoped>

</style>