<template>
    <div class="calendar">
        <v-layout justify-space-between row>
            <v-flex class="arrow-left" xs3>
                <v-btn @click="navigateToLastMonth">
                    <v-icon>arrow_left</v-icon>
                </v-btn>
            </v-flex>
            <v-flex class="today-date" xs6>
                {{firstDayOfCurrentWatchingMonth.getFullYear()}}年{{firstDayOfCurrentWatchingMonth.getMonth()+1}}月
            </v-flex>
            <v-flex class="arrow-right" xs3>
                <v-btn @click="navigateToNextMonth">
                    <v-icon>arrow_right</v-icon>
                </v-btn>
            </v-flex>
        </v-layout>
        <v-layout row wrap>
            <Day :key="-i" class="day-empty" v-for="i in marginDaysBeforeFirstDay"></Day>
            <Day :class="{watching:isSameDate(day,currentWatchingDate)}"
                 :content="day"
                 :key="day.getDate()"
                 @click="daySelected"
                 v-for="day in daysInThisMonth"></Day>
            <Day :key="i+31" class="day-empty" v-for="i in marginDaysAfterLastDay"></Day>
        </v-layout>
    </div>
</template>

<script lang="ts">
    import Component from 'nuxt-class-component';
    import Vue from 'vue';
    import { Emit, Prop } from 'vue-property-decorator';
    import { clone } from '../../tools/clone';
    import Day from './day.vue';
    import { isSameDate } from '../../../shared/tools/date';

    @Component({
        components: { Day },
        methods: { isSameDate }
    })
    export default class Calendar extends Vue {
        @Prop({ default: new Date() })
        initialDate: Date;

        firstDayOfCurrentWatchingMonth: Date = new Date();

        currentWatchingDate: Date = new Date();

        created() {
            this.firstDayOfCurrentWatchingMonth = this.initialDate;
            this.firstDayOfCurrentWatchingMonth.setDate(1);
        }

        get marginDaysBeforeFirstDay(): number {
            let firstDayInThisMonth = this.firstDayOfCurrentWatchingMonth;
            return firstDayInThisMonth.getDay();
        }

        get daysInThisMonth(): Array<Date> {
            let result = [];
            let firstDay = this.firstDayOfCurrentWatchingMonth;
            for (let currentDay = clone(firstDay); currentDay.getMonth() == firstDay.getMonth(); currentDay.setDate(currentDay.getDate() + 1)) {
                result.push(clone(currentDay));
            }
            return result;
        }

        get marginDaysAfterLastDay(): number {
            let lastDayInThisMonth = this.firstDayOfCurrentWatchingMonth;
            lastDayInThisMonth.setMonth(lastDayInThisMonth.getMonth() + 1);
            lastDayInThisMonth.setDate(0);
            return 6 - lastDayInThisMonth.getDay();
        }

        navigateToNextMonth() {
            this.firstDayOfCurrentWatchingMonth = new Date(this.firstDayOfCurrentWatchingMonth.getFullYear(), this.firstDayOfCurrentWatchingMonth.getMonth() + 1, 1);
        }

        navigateToLastMonth() {
            this.firstDayOfCurrentWatchingMonth = new Date(this.firstDayOfCurrentWatchingMonth.getFullYear(), this.firstDayOfCurrentWatchingMonth.getMonth() - 1, 1);
        }

        @Emit('daySelected')
        daySelected(day: Date) {
            this.currentWatchingDate = day;
        }
    };
</script>

<style scoped lang="stylus">
    .calendar {
        justify-content: flex-start;
        padding 10px
    }

    .arrow-right,
    .arrow-left {
        height 50px
        line-height 50px
        text-align center
    }

    .today-date {
        text-align center
        line-height 50px
    }

    .watching {
        border solid 1px #ff9752
    }

    button.btn {
        max-width 50px
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
</style>
