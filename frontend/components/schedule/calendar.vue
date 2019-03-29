<template>
    <div class="calendar">
        <v-layout justify-space-between row v-touch="{
                    left: navigateToNextMonth,
                    right: navigateToLastMonth
                }">
            <v-flex class="arrow-left text-xs-center" sm1 xs2>
                <v-btn @click="navigateToLastMonth" fab small>
                    <v-icon>arrow_left</v-icon>
                </v-btn>
            </v-flex>
            <v-flex class="today-date" xs8>
                {{format(firstDayOfCurrentWatchingMonth,'yyyy 年 MM 月')}}
            </v-flex>
            <v-flex class="arrow-right text-xs-center" sm1 xs2>
                <v-btn @click="navigateToNextMonth" fab small>
                    <v-icon>arrow_right</v-icon>
                </v-btn>
            </v-flex>
        </v-layout>
        <v-slide-x-transition class="row wrap"
                              group
                              hide-on-leave
                              tag="v-layout"
                              v-touch="{left: navigateToNextMonth,right: navigateToLastMonth}">
            <v-flex :key="day" class="day-name text-xs-center" v-for="day in DAY_CHINESES">{{day}}</v-flex>
            <Day :key="-i" class="day-empty" v-for="i in marginDaysBeforeFirstDay"></Day>
            <Day :class="{watching:isSameDay(currentWatchingDate,day)}"
                 :date="some(day)"
                 :key="day.getDate()"
                 @click="daySelected"
                 v-for="day in daysInThisMonth"></Day>
            <Day :key="i+31" class="day-empty" v-for="i in marginDaysAfterLastDay"></Day>
        </v-slide-x-transition>
    </div>
</template>

<script lang="ts">
    import {Component, Emit, Prop, Vue} from "vue-property-decorator";
    import Day from "~/components/schedule/day.vue";
    import {some} from "fp-ts/lib/Option";
    import {DayService} from "~/tools/day";
    import {addMonths, eachDayOfInterval, format, isSameDay, lastDayOfMonth, startOfMonth, subMonths} from "date-fns";

    @Component({
        components: {
            Day
        },
        methods: {
            some,
            format,
            isSameDay
        }
    })
    export default class Calendar extends Vue {
        DAY_CHINESES = DayService.DAY_NUMBER_TO_CHINESE.toArray();

        async fetch(context: { store: any, params: any }) {
            await context.store.dispatch("course/fetchCourses");
        }

        @Prop({default: () => new Date()})
        initialDate!: Date;

        firstDayOfCurrentWatchingMonth = startOfMonth(new Date());

        currentWatchingDate = new Date();

        get marginDaysBeforeFirstDay(): number {
            return this.firstDayOfCurrentWatchingMonth.getDay();
        }

        get marginDaysAfterLastDay(): number {
            let lastDayInThisMonth = lastDayOfMonth(this.firstDayOfCurrentWatchingMonth);
            return 6 - lastDayInThisMonth.getDay();
        }

        get daysInThisMonth(): Array<Date> {
            return eachDayOfInterval({
                start: this.firstDayOfCurrentWatchingMonth,
                end: lastDayOfMonth(this.firstDayOfCurrentWatchingMonth)
            });
        }

        navigateToLastMonth() {
            this.firstDayOfCurrentWatchingMonth = subMonths(this.firstDayOfCurrentWatchingMonth, 1);
        }

        navigateToNextMonth() {
            this.firstDayOfCurrentWatchingMonth = addMonths(this.firstDayOfCurrentWatchingMonth, 1)
        }

        @Emit('daySelected')
        daySelected(day: Date) {
            this.currentWatchingDate = day;
        }
    };
</script>

<style scoped>
    .calendar {
        justify-content: flex-start;
        padding: 10px;
        max-width: 600px;
    }

    .today-date {
        text-align: center;
        line-height: 50px;
    }

    .watching {
        border: solid 1px #ff9752;
    }

    .month-complete-item {
        transition: all 1s;
        display: inline-block;
        margin-right: 10px;
    }

    .month-complete-enter, .list-complete-leave-to {
        opacity: 0;
        transform: translateY(30px);
    }

    .month-complete-leave-active {
        position: absolute;
    }

    .day-name {
        flex: 14.28%;
    }

    .fade-enter-active, .fade-leave-active {
        transition: opacity .5s;
    }

    .fade-enter, .fade-leave-active {
        opacity: 0;
    }
</style>
