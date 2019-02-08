<template>
    <v-form>
        <v-container fluid grid-list-md text-xs-center>
            <v-layout row wrap>
                <v-flex xs12>
                    <v-text-field
                            label="假期名称"
                            required
                            v-model="name"
                    ></v-text-field>
                </v-flex>
                <v-flex sm6 xs12>
                    开始日期
                    <br>
                    <v-date-picker color="primary" locale="zh-cn" v-model="begin"></v-date-picker>
                </v-flex>
                <v-flex sm6 xs12>
                    结束日期
                    <br>
                    <v-date-picker color="green lighten-1" locale="zh-cn" v-model="end"></v-date-picker>
                </v-flex>
                <v-flex xs12>
                    <v-expansion-panel>
                        <v-expansion-panel-content
                                :key="shift.from.toString()"
                                v-for="(shift,index) in shifts">
                            <div slot="header">
                                {{shift.from.toLocaleDateString()}} =>
                                {{shift.to.toLocaleDateString()}}
                            </div>
                            <ShiftEditor :data="shift"
                                         @remove="removeShift(index)"
                                         @save="(shift) => updateShift(index,shift)"
                            ></ShiftEditor>
                        </v-expansion-panel-content>
                    </v-expansion-panel>
                </v-flex>
                <v-flex xs12>
                    <v-layout row wrap>
                        <v-flex sm4 xs12>
                            <v-btn @click="addShift" block color="primary">添加调休</v-btn>
                        </v-flex>
                        <v-flex sm4 xs6>
                            <v-btn @click="remove" block color="error">删除</v-btn>
                        </v-flex>
                        <v-flex sm4 xs6>
                            <v-btn @click="save(holiday)" block color="primary">确定</v-btn>
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
    import {Holiday, HolidayService, HolidayWithShift} from "../../../shared/model/semester/holiday/holiday";
    import {Shift} from "../../../shared/model/semester/holiday/shift/shift";
    import ShiftEditor from "~/components/admin/shiftEditor.vue";

    @Component({
        components: {ShiftEditor}
    })
    export default class HolidayEditor extends Vue {
        @Prop({default: null})
        data!: Holiday | HolidayWithShift;

        name: string = "";
        begin: string = "";
        end: string = "";
        shifts: Array<Shift> = [];

        mounted() {
            this.name = this.data.name;
            this.begin = this.data.begin.toLocaleDateString().split('/').map(it => it.length < 2 ? '0' + it : it).join('-');
            this.end = this.data.end.toLocaleDateString().split('/').map(it => it.length < 2 ? '0' + it : it).join('-');
            if (HolidayService.hasShift(this.data)) {
                this.shifts = this.data.shifts;
            }
        }

        get holiday(): Holiday | HolidayWithShift {
            if (this.shifts.length !== 0) {
                return {
                    name: this.name,
                    begin: new Date(this.begin),
                    end: new Date(this.end),
                    shifts: this.shifts
                }
            } else {
                return {
                    name: this.name,
                    begin: new Date(this.begin),
                    end: new Date(this.end)
                }
            }
        }

        @Emit('save')
        save(holiday: Holiday | HolidayWithShift) {
        }

        @Emit('remove')
        remove() {
        }

        addShift() {
            this.shifts.push({
                from: new Date(),
                to: new Date()
            });
        }

        updateShift(index: number, shift: Shift) {
            this.shifts.splice(index, 1, shift);
        }

        removeShift(index: number) {
            this.shifts.splice(index);
        }
    }
</script>

<style scoped>

</style>