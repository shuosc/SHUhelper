<template>
    <v-form>
        <v-container fluid grid-list-md text-xs-center>
            <v-layout row wrap>
                <v-flex sm6 xs12>
                    休息
                    <br>
                    <v-date-picker color="primary" locale="zh-cn" v-model="from"></v-date-picker>
                </v-flex>
                <v-flex sm6 xs12>
                    补上课
                    <br>
                    <v-date-picker color="green lighten-1" locale="zh-cn" v-model="to"></v-date-picker>
                </v-flex>
                <v-flex xs12>
                    <v-layout row wrap>
                        <v-flex xs6>
                            <v-btn @click="remove" block color="error">删除</v-btn>
                        </v-flex>
                        <v-flex xs6>
                            <v-btn @click="save(shift)" block color="primary">确定</v-btn>
                        </v-flex>
                    </v-layout>
                </v-flex>
            </v-layout>
        </v-container>
    </v-form>
</template>

<script lang="ts">
    import Component from 'nuxt-class-component';
    import {Emit, Prop, Vue} from 'vue-property-decorator';
    import {Shift} from "../../../shared/model/semester/holiday/shift/shift";

    @Component
    export default class ShiftEditor extends Vue {
        @Prop({default: null})
        data!: Shift;

        from: string = "";
        to: string = "";

        mounted() {
            this.from = this.data.from.toLocaleDateString().split('/').map(it => it.length < 2 ? '0' + it : it).join('-');
            this.to = this.data.to.toLocaleDateString().split('/').map(it => it.length < 2 ? '0' + it : it).join('-');
        }

        get shift(): Shift {
            return {
                from: new Date(this.from),
                to: new Date(this.to)
            }
        }

        @Emit('save')
        save(shift: Shift) {
        }

        @Emit('remove')
        remove() {
        }
    }
</script>

<style scoped>

</style>