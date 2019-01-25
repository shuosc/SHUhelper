<template>
    <v-card class="pa-0">
        <v-card-title class="pa-0" primary-title>
            <v-container class="pa-3">
                <v-layout align-center row wrap>
                    <v-flex fill-height xs1>
                        <v-layout align-center justify-center>
                            <v-avatar :size="avatarSize()">
                                <v-icon class="white--text blue" medium>event</v-icon>
                            </v-avatar>
                        </v-layout>
                    </v-flex>
                    <v-divider class="mx-3" inset vertical></v-divider>
                    <v-flex xs9>
                        <v-layout row wrap>
                            <v-flex xs12>
                                今天是{{now.getFullYear()}}年{{now.getMonth()+1}}月{{now.getDate()}}日
                                周{{dayNumberToChinese(now.getDay()).value}}
                            </v-flex>
                            <template v-if="!currentSemester.isNull">
                                <v-flex xs12>
                                    是{{currentSemester.value.name}}
                                    <template v-if="!currentWeekIndex.isNull">的第{{ currentWeekIndex.value }}周</template>
                                </v-flex>
                                <v-flex v-if="!currentHoliday.isNull" xs12>
                                    现在正在放{{currentHoliday.value.name}}!
                                </v-flex>
                                <v-flex v-else-if="!nextHoliday.isNull" xs12>
                                    <template v-if="daysTo(now,nextHoliday.value) !== 0">
                                        距离下个假期{{nextHoliday.value.name}}还有{{daysTo(now,nextHoliday.value)}}天
                                    </template>
                                    <template v-else>下个假期{{nextHoliday.value.name}}明天就开始！</template>
                                </v-flex>
                                <v-flex xs12>
                                    <v-layout row wrap>
                                        <v-flex xs12>
                                            <v-progress-linear
                                                    v-model="finishedDaysPercentage.value"></v-progress-linear>
                                        </v-flex>
                                        <v-flex xs12>
                                            已经过了{{totalWorkingDayCountInThisSemester.value}}个工作日中的{{passedWorkingDayCountInThisSemester.value}}天
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
    import {DayService} from "../../../shared/tools/dateTime/day/day";
    import {Semester, SemesterService} from "../../../shared/model/semester/semester";
    import * as semesterModule from '~/store/modules/semester';
    import {just, Maybe} from "../../../shared/tools/functools/maybe";
    import * as _ from "lodash";
    import {Holiday, HolidayWithShift} from "../../../shared/model/semester/holiday/holiday";
    import {DateRangeService} from "../../../shared/model/dateRange/dateRange";
    import {find} from "../../../shared/tools/functools/find";
    import {toPercent} from "~/tools/toPercent";
    import dayNumberToChinese = DayService.dayNumberToChinese;
    import daysTo = DateRangeService.daysTo;

    const SemesterNamespace = namespace(semesterModule.name);

    @Component({
        methods: {
            avatarSize,
            dayNumberToChinese,
            daysTo
        }
    })
    export default class DateInfo extends Vue {
        now = new Date(2018, 11, 3);
        @SemesterNamespace.Getter getSemesterForDate!: (date: Date) => Maybe<Semester>;

        mounted() {
            setInterval(() => {
                this.now = new Date();
            }, 1000);
        }

        get currentSemester() {
            return this.getSemesterForDate(this.now);
        }

        get currentWeekIndex(): Maybe<number> {
            const getCurrentWeekIndex = _.partial(SemesterService.getWeekIndex, _, this.now);
            return this.currentSemester
                .map(getCurrentWeekIndex)
                .flatMap(it => it === 0 ? just<number>(null) : just(it));
        }

        get nextHoliday(): Maybe<Holiday | HolidayWithShift> {
            const nextFromNow = _.partial(DateRangeService.nextFromDate, _, this.now);
            return this.currentSemester.flatMap(it => nextFromNow(it.holidays));
        }

        get currentHoliday(): Maybe<Holiday | HolidayWithShift> {
            const nowIn = _.partial(DateRangeService.isDateIn, _, this.now);
            return this.currentSemester.flatMap(it => find(it.holidays, nowIn));
        }

        get passedWorkingDayCountInThisSemester(): Maybe<number> {
            const passedWorkingDayCount = (semester: Semester) => SemesterService.getWorkingDayCount(semester, semester.begin, this.now);
            return this.currentSemester.map(passedWorkingDayCount);
        }

        get totalWorkingDayCountInThisSemester(): Maybe<number> {
            return this.currentSemester.map(SemesterService.getTotalWorkingDayCount);
        }

        get finishedDaysPercentage(): Maybe<number> {
            // Silly Webstorm failed to infer _.curry's type
            // noinspection TypeScriptValidateTypes
            return just(_.curry(toPercent))
                .apply(this.passedWorkingDayCountInThisSemester)
                .apply(this.totalWorkingDayCountInThisSemester);
        }
    }
</script>

<style scoped>
</style>