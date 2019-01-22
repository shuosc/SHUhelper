<template>
    <v-card class="pa-0">
        <v-card-title class="pa-0" primary-title>
            <v-container class="pa-3">
                <v-layout align-center row wrap>
                    <v-flex fill-height xs1>
                        <v-layout align-center justify-center>
                            <v-avatar :size="avatarSize">
                                <v-icon class="white--text blue" medium>event</v-icon>
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
                                今天是
                                {{today.getFullYear()}}年{{today.getMonth()+1}}月{{today.getDate()}}日
                                周{{DAY_NUMBER_TO_CHINESE[today.getDay()]}}
                            </v-flex>
                            <v-flex xs12>
                                是{{thisSemester.name}}
                                <template v-if="getWeekIndex(thisSemester,today) !== 0">
                                    的第{{ getWeekIndex(thisSemester,today) }}周
                                </template>
                            </v-flex>
                            <v-flex v-if="nearestHoliday.value !== null" xs12>
                                <template v-if="daysTo(today,nearestHoliday.value) !== 0">距离</template>
                                下个假期 {{nearestHoliday.value.name}}
                                <template v-if="daysTo(today,nearestHoliday.value) !== 0">
                                    还有{{daysTo(today,nearestHoliday.value)}}天
                                </template>
                                <template v-else>明天就开始！</template>
                            </v-flex>
                            <v-flex v-if="inHoliday.value !== null" xs12>
                                现在正在放{{inHoliday.value.name}}!
                            </v-flex>
                            <v-flex xs12>
                                <v-progress-linear v-model="finishedDaysPercentage"></v-progress-linear>
                            </v-flex>
                            <v-flex xs12>
                                已经过了{{getWorkingDayCount(thisSemester)}}个工作日中的{{getWorkingDayCount(thisSemester)-getWorkingDayCountFrom(thisSemester,today)}}天
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
    import * as _ from "lodash";
    import * as semesters from '~/store/modules/semester';
    import {DAY_NUMBER_TO_CHINESE} from '../../../shared/tools/date/date';
    import {Semester, SemesterService} from "../../../shared/model/semester/semester";
    import {DateRangeService} from "../../../shared/model/dateRange/dateRange";
    import {Holiday} from "../../../shared/model/semester/holiday/holiday";
    import {Maybe} from "../../../shared/tools/functools/maybe";
    import {find} from "../../../shared/tools/functools/find";
    import getWeekIndex = SemesterService.getWeekIndex;
    import getWorkingDayCount = SemesterService.getWorkingDayCount;
    import getWorkingDayCountFrom = SemesterService.getWorkingDayCountFrom;
    import daysTo = DateRangeService.daysTo;

    const Semesters = namespace(semesters.name);
    declare const process: { client: boolean };
    @Component({
        methods: {
            getWeekIndex,
            daysTo,
            getWorkingDayCount,
            getWorkingDayCountFrom
        }
    })
    export default class DateInfo extends Vue {
        DAY_NUMBER_TO_CHINESE = DAY_NUMBER_TO_CHINESE;
        @Semesters.Getter getSemesterForDate: any;
        @Semesters.Getter getSemester: any;
        @Semesters.State semesters: any;

        get today(): Date {
            return new Date();
        }


        get thisSemester(): Semester {
            return this.getSemesterForDate(this.today).value;
        }


        get nearestHoliday(): Maybe<Holiday> {
            return DateRangeService.nearestToDate(this.thisSemester.holidays, this.today);
        }

        get inHoliday(): Maybe<Holiday> {
            const isTodayIn = _.partial(DateRangeService.isDateIn, _, this.today);
            return find(this.thisSemester.holidays, isTodayIn);
        }

        get finishedDaysPercentage() {
            return (getWorkingDayCount(this.thisSemester) - getWorkingDayCountFrom(this.thisSemester, this.today)) / getWorkingDayCount(this.thisSemester) * 100;
        }

        get avatarSize(): number {
            if (process.client) {
                return window.innerWidth > 425 ? 60 : 40;
            }
            return 50;
        }
    }
</script>

<style scoped>
</style>