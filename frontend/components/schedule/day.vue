<template>
    <v-flex :class="{today: isToday,'non-empty': content!=null}" @click="clicked" class="day">
        <v-container align-center fill-height justify-center>
            <v-layout column>
                <v-flex class="date-number-wrapper text-xs-center">
                    <span class="date-number">{{content == null ? '' :content.getDate()}}</span>
                </v-flex>
                <v-flex class="dots text-xs-center">
                    <template v-if="!isHoliday(content)">
                        <v-layout align-center justify-center row wrap>
                        <span :style="{background:course.color}" class="dot"
                              v-for="course in getCoursesForDate(content)"></span>
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
    import {isSameDate} from '../../../shared/tools/date';
    import * as courses from '~/store/modules/course';
    import * as semester from '~/store/modules/semester';

    const Semester = namespace(semester.name);
    const Courses = namespace(courses.name);

    @Component
    export default class Day extends Vue {
        @Prop({default: null, type: Date})
        content!: Date;
        @Courses.Getter getCoursesForDate: any;
        @Semester.Getter isHoliday: any;

        get isToday(): boolean {
            if (this.content === null) {
                return false;
            } else {
                const today = new Date();
                return isSameDate(today, this.content);
            }
        }

        clicked() {
            if (this.content !== null)
                this.$emit('click', this.content);
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
