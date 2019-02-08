<template>
    <v-form class="indigo">
        <v-container fluid grid-list-md text-xs-center>
            <v-layout row wrap>
                <v-flex xs12>
                    <v-text-field
                            label="学期名称"
                            required
                            v-model="name"
                    ></v-text-field>
                </v-flex>
                <v-flex sm6 xs12>
                    开始日期{{new Date(this.begin)}}
                    <br>
                    <v-date-picker :allowed-dates="(date) => new Date(date).getDay() === 1" color="primary"
                                   locale="zh-cn"
                                   v-model="begin"></v-date-picker>
                </v-flex>
                <v-flex sm6 xs12>
                    结束日期{{new Date(this.end)}}
                    <br>
                    <v-date-picker
                            :allowed-dates="(date) => (new Date(date).getDay() === 5) && (new Date(date) > new Date(begin))"
                            color="green lighten-1"
                            locale="zh-cn"
                            v-model="end"
                    ></v-date-picker>
                </v-flex>
                <v-flex xs12>
                    <v-expansion-panel>
                        <v-expansion-panel-content
                                :key="holiday.name"
                                v-for="(holiday,index) in holidays">
                            <div slot="header">{{holiday.name}}</div>
                            <HolidayEditor :data="holiday"
                                           @remove="removeHoliday(index)"
                                           @save="(holiday) => updateHoliday(index,holiday)"
                            ></HolidayEditor>
                        </v-expansion-panel-content>
                    </v-expansion-panel>
                </v-flex>
                <v-layout row wrap>
                    <v-flex sm4 xs12>
                        <v-btn @click="addHoliday" block color="primary">添加假期</v-btn>
                    </v-flex>
                    <v-flex sm4 xs6>
                        <v-btn @click="remove" block color="error">删除</v-btn>
                    </v-flex>
                    <v-flex sm4 xs6>
                        <v-btn @click="save" block color="primary">确定</v-btn>
                    </v-flex>
                </v-layout>
            </v-layout>
        </v-container>
    </v-form>
</template>

<script lang="ts">
    import Component, {namespace} from 'nuxt-class-component';
    import {Prop, Vue} from 'vue-property-decorator';
    import {Semester} from "../../../shared/model/semester/semester";
    import HolidayEditor from "~/components/admin/holidayEditor.vue";
    import * as semesterModule from '~/store/modules/semester';
    import {Holiday, HolidayWithShift} from "../../../shared/model/semester/holiday/holiday";

    const SemesterNamespace = namespace(semesterModule.name);
    @Component({
        components: {HolidayEditor}
    })
    export default class SemesterEditor extends Vue {
        @SemesterNamespace.Action putSemester!: (payload: { semester: Semester }) => void;
        @SemesterNamespace.Action deleteSemester!: (payload: { semester: Semester }) => void;

        @Prop({default: null})
        data!: Semester;

        name: string = "";
        begin: string = "";
        end: string = "";
        holidays: Array<Holiday | HolidayWithShift> = [];

        mounted() {
            this.name = this.data.name;
            this.begin = this.data.begin.toLocaleDateString().split('/').map(it => it.length < 2 ? '0' + it : it).join('-');
            this.end = this.data.end.toLocaleDateString().split('/').map(it => it.length < 2 ? '0' + it : it).join('-');
            this.holidays = this.data.holidays;
        }

        save() {
            this.putSemester({
                semester: {
                    _id: this.data._id,
                    name: this.name,
                    begin: new Date(this.begin),
                    end: new Date(this.end),
                    holidays: this.holidays
                }
            });
        }

        updateHoliday(index: number, holiday: Holiday | HolidayWithShift) {
            this.holidays.splice(index, 1, holiday);
        }

        addHoliday() {
            this.holidays.push({
                name: "新的假期",
                begin: new Date(),
                end: new Date()
            });
        }

        removeHoliday(index: number) {
            this.holidays.splice(index);
        }

        remove() {
            this.deleteSemester({semester: this.data});
        }
    }
</script>

<style scoped>

</style>