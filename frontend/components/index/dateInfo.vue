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
                    <v-divider class="mx-3" inset vertical>
                    </v-divider>
                    <v-flex xs9>
                        <v-layout row wrap>
                            <v-flex xs12>
                                今天是{{format(now,"yyyy年MM月dd日")}} 周{{dayNumberToChinese(now.getDay()).toNullable()}}
                            </v-flex>
                            <v-flex v-if="currentDateInSemester.isSome()" xs12>
                                是 {{currentDateInSemester.map(it => it.semester.name).toNullable()}}
                                <template v-if="currentDateInSemester.map(getWorkWeekIndex).getOrElse(0) !== 0">
                                    的第 {{currentDateInSemester.map(getWorkWeekIndex).toNullable()}} 周
                                </template>
                            </v-flex>
                            <v-flex v-if="currentDateInSemester.chain(getHoliday).isSome()" xs12>
                                现在正在放{{currentDateInSemester.chain(getHoliday).map(it => it.name).toNullable()}}!
                            </v-flex>
                            <v-flex v-else-if="nextHoliday.isSome()" xs12>
                                <template v-if="daysToNextHoliday.toNullable() !== 0">
                                    距离下个假期 {{nextHoliday.map(it => it.name).toNullable()}} 还有
                                    {{daysToNextHoliday.toNullable()}} 天
                                </template>
                                <template v-else>下个假期 {{nextHoliday.map(it => it.name).toNullable()}} 明天就开始！</template>
                            </v-flex>
                            <v-flex v-if="finishedDaysPercentage.isSome()" xs12>
                                <v-progress-linear v-model="finishedDaysPercentage.toNullable()"></v-progress-linear>
                            </v-flex>
                            <v-flex v-if="finishedDaysPercentage.isSome()" xs12>
                                已经过了 {{totalWorkingDays.toNullable()}} 个工作日中的 {{finishedWorkingDays.toNullable()}} 天
                            </v-flex>
                        </v-layout>
                    </v-flex>
                </v-layout>
            </v-container>
        </v-card-title>
    </v-card>
</template>


<script lang="ts">

    import {namespace} from "~/node_modules/vuex-class";
    import {Component, Vue} from "~/node_modules/vue-property-decorator";
    import {DayService} from "~/tools/day";
    import {avatarSize} from "~/tools/avatarSize";
    import {DateTimeInSemester, DateTimeInSemesterService} from "~/service/dateTimeInSemester.service";
    import {SemesterService} from "~/service/semester.service";
    import {option, Option, some} from "fp-ts/lib/Option";

    import dayNumberToChinese = DayService.dayNumberToChinese;
    import getWorkingDayCount = SemesterService.getWorkingDayCount;
    import getWorkWeekIndex = DateTimeInSemesterService.getWorkWeekIndex;
    import getHoliday = DateTimeInSemesterService.getHoliday;
    import {Holiday} from "../../../shared/model/semester/holiday/holiday";
    import getNextHoliday = DateTimeInSemesterService.getNextHoliday;
    import {liftA2, liftA3} from "~/node_modules/fp-ts/lib/Apply";
    import {curry} from "~/node_modules/fp-ts/lib/function";
    import {toPercent} from "~/tools/toPercent";
    import {eachDayOfInterval, format} from "date-fns";
    import {Semester} from "../../../shared/model/semester/semester";


    const SemesterNamespace = namespace("semester");
    @Component({
        methods: {
            avatarSize,
            dayNumberToChinese,
            getWorkWeekIndex,
            getHoliday,
            getWorkingDayCount,
            format
        }
    })
    export default class DateInfo extends Vue {
        @SemesterNamespace.Getter semesterForDate!: (date: Date) => Option<Semester>;
        @SemesterNamespace.Action fetchCurrent!: () => void;
        now = new Date();

        async mounted() {
            await this.fetchCurrent();
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

        get nextHoliday(): Option<Holiday> {
            return this.currentDateInSemester.chain(getNextHoliday);
        }

        get daysToNextHoliday(): Option<number> {
            return this.nextHoliday.map(it => {
                return eachDayOfInterval({start: this.now, end: it.start}).length;
            });
        }

        get finishedWorkingDays(): Option<number> {
            return liftA3(option)(curry(SemesterService.getWorkingDayCount))(this.current)(this.current.map(it => it.start))(some(this.now));
        }

        get totalWorkingDays(): Option<number> {
            return this.current.map(SemesterService.getTotalWorkingDayCount)
        }

        get finishedDaysPercentage(): Option<number> {
            return liftA2(option)(curry(toPercent))(this.finishedWorkingDays)(this.totalWorkingDays);
        }
    }
</script>
