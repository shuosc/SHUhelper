<template>
    <v-flex :class="{today: isToday,'non-empty': content!=null}" @click="clicked" class="day">
        {{content == null ? '' :content.getDate()}}
    </v-flex>
</template>

<script lang="ts">
    import Component from 'nuxt-class-component';
    import Vue from 'vue';
    import { Prop } from 'vue-property-decorator';
    import { isSameDate } from '../../../shared/tools/date';

    @Component
    export default class Day extends Vue {
        @Prop({ default: null, type: Date })
        content: Date | null;

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
        display flex;
        font-size 15pt;
        justify-content center;
        align-items center;
        min-height 60px;
        border-radius 4px
        user-select none

        &.non-empty {
            cursor pointer

            &:hover {
                color white
                background #303030
            }
        }
    }

    .today {
        color #6eb5ff

        &.non-empty:hover {
            color #333d67
            background #5a71bb
        }
    }
</style>
