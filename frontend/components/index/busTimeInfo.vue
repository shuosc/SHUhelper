<template>
    <v-card class="pa-0 mt-2">
        <v-card-title class="pa-0" primary-title>
            <v-container class="pa-3">
                <v-layout align-center row wrap>
                    <v-flex fill-height xs1>
                        <v-layout align-center justify-center>
                            <v-avatar :size="avatarSize() ">
                                <v-icon class="white--text red lighten-1" medium>directions_bus</v-icon>
                            </v-avatar>
                        </v-layout>
                    </v-flex>
                    <v-divider class="mx-3" inset vertical></v-divider>
                    <v-flex xs9>
                        <v-layout row wrap>
                            <v-flex class="pa-1" sm6 xs12>
                                <v-select :items="CampusRepository.all"
                                          item-text="name"
                                          item-value="id"
                                          label="起始"
                                          v-model="fromCampusId">
                                </v-select>
                            </v-flex>
                            <v-flex class="pa-1" sm6 xs12>
                                <v-select :items="CampusRepository.all"
                                          item-text="name"
                                          item-value="id"
                                          label="终点"
                                          v-model="toCampusId">
                                </v-select>
                            </v-flex>
                            <v-flex v-if="nextByFromTo.isNone()" xs12>
                                今天此线路最后一辆校车已经走了哦,下次请早点来吧！
                            </v-flex>
                            <v-flex v-else xs12>
                                <v-layout align-center class="mb-2" row wrap>
                                    <v-flex sm1 v-if="currentWaitingPercentage.isSome()" xs2>
                                        <v-progress-circular
                                                :size="35"
                                                :value="currentWaitingPercentage.toNullable()"
                                                :width="2"
                                                color="green">
                                            {{timeStringToNext.toNullable()}}
                                        </v-progress-circular>
                                    </v-flex>
                                    <v-flex sm11 xs10>
                                        此线路下一班校车还有{{chineseTimeStringToNext.toNullable()}}
                                    </v-flex>
                                </v-layout>
                            </v-flex>
                            <v-flex xs12>
                                <v-expansion-panel expand v-model="expanded">
                                    <v-expansion-panel-content>
                                        <div slot="header" v-if="expanded[0]">收起</div>
                                        <div slot="header" v-else>查看该线路所有班次</div>
                                        <v-radio-group class="ml-3" row v-model="schoolBusRoutineType">
                                            <v-radio :value="SchoolBusRoutineType.WorkingDay" color="primary"
                                                     label="工作日"></v-radio>
                                            <v-radio :value="SchoolBusRoutineType.NonWorkingDay" color="primary"
                                                     label="节假日"></v-radio>
                                        </v-radio-group>
                                        <v-data-table
                                                :headers="[{ text: '班次', value: 'index' },{ text: '时间', value: 'time' }]"
                                                :items="timeTable.map((it,index) => {return {index:index+1,time:format(it,'HH:mm')}})"
                                                class="elevation-1">
                                            <template slot="items" slot-scope="props">
                                                <td>{{ props.item.index }}</td>
                                                <td>{{ props.item.time }}</td>
                                            </template>
                                        </v-data-table>
                                    </v-expansion-panel-content>
                                </v-expansion-panel>
                            </v-flex>
                        </v-layout>
                    </v-flex>
                </v-layout>
            </v-container>
        </v-card-title>
    </v-card>
</template>

<script lang="ts">

    import {namespace} from "vuex-class";
    import {Component, Vue, Watch} from "~/node_modules/vue-property-decorator";
    import {avatarSize} from "~/tools/avatarSize";
    import {none, option, Option} from "~/node_modules/fp-ts/lib/Option";
    import {Semester} from "../../../shared/model/semester/semester";
    import {SchoolBusRepository} from "~/repository/schoolBus.repository";
    import {SchoolBusRoutine} from "../../../shared/model/schoolBus/schoolBus";
    import {SchoolBusService} from "~/service/schoolBus";
    import {liftA2, liftA3} from "~/node_modules/fp-ts/lib/Apply";
    import {curry} from "~/node_modules/fp-ts/lib/function";
    import {CampusRepository} from "~/tools/campus.repository";
    import {SchoolBusRoutineType} from "~/tools/schoolBus";
    import {differenceInMinutes, format} from "date-fns";
    import {_, partial} from "~/tools/partial";
    import {toPercent} from "~/tools/toPercent";
    import {differenceInMinutes as fpDifferenceInMinutes} from "date-fns/fp"
    import {DateTimeInSemester} from "~/service/dateTimeInSemester.service";
    import {extractTime} from "~/tools/dateTime";

    const SemesterNamespace = namespace("semester");

    @Component({
        methods: {
            avatarSize,
            format
        }
    })
    export default class BusTimeInfo extends Vue {
        CampusRepository = CampusRepository;
        SchoolBusRoutineType = SchoolBusRoutineType;

        @SemesterNamespace.Getter semesterForDate!: (date: Date) => Option<Semester>;
        @SemesterNamespace.Action fetchCurrent!: () => void;
        @SemesterNamespace.Action fetchSemester!: (payload: { forDate: Date }) => void;


        now = new Date();
        schoolBusRoutineType: SchoolBusRoutineType = SchoolBusRoutineType.WorkingDay;
        fromCampusId: number = 0;
        toCampusId: number = 1;
        expanded = [false];

        mounted() {
            setInterval(() => {
                this.now = new Date();
            }, 1000);
        }

        get timeTable(): Array<Date> {
            const fromCampus = CampusRepository.getById(this.fromCampusId).toNullable();
            const toCampus = CampusRepository.getById(this.toCampusId).toNullable();
            return SchoolBusRepository
                .getByFromTo(fromCampus, toCampus, this.schoolBusRoutineType as any)
                .map((schoolBus: SchoolBusRoutine) => SchoolBusService.startTimeInCampus(schoolBus, fromCampus).toNullable());
        }

        @Watch('fromCampusId', {immediate: true, deep: true})
        onFromCampusId() {
            if (this.fromCampusId === this.toCampusId) {
                this.toCampusId = (this.fromCampusId + 1) % CampusRepository.all.length;
            }
        }

        @Watch('toCampusId', {immediate: true, deep: true})
        onToCampusId() {
            if (this.fromCampusId === this.toCampusId) {
                this.fromCampusId = (this.toCampusId + 1) % CampusRepository.all.length;
            }
        }

        get fromCampus() {
            return CampusRepository.getById(this.fromCampusId);
        }

        get toCampus() {
            return CampusRepository.getById(this.toCampusId);
        }

        get nextByFromTo(): Option<SchoolBusRoutine> {
            return liftA3(option)(curry(SchoolBusRepository.getNextByFromTo))(this.fromCampus)(this.toCampus)(this.currentDateInSemester).getOrElse(none);
        }

        get lastByFromTo(): Option<SchoolBusRoutine> {
            return liftA3(option)(curry(SchoolBusRepository.getLastByFromTo))(this.fromCampus)(this.toCampus)(this.currentDateInSemester).getOrElse(none);
        }

        get minutesToNext(): Option<number> {
            const nextStartTime: Option<Date> = liftA2(option)(curry(SchoolBusService.startTimeInCampus))(this.nextByFromTo)(this.fromCampus).getOrElse(none);
            return nextStartTime.map(partial(differenceInMinutes, _, extractTime(this.now)));
        }

        get chineseTimeStringToNext(): Option<string> {
            return this.minutesToNext.map(it => {
                const hours = Math.floor(it / 60);
                const minutes = it - hours * 60;
                return (hours !== 0 ? `${hours}小时` : '') + `${minutes}分钟`;
            });
        }

        get timeStringToNext(): Option<string> {
            return this.minutesToNext.map(it => {
                const hours = Math.floor(it / 60);
                const minutes = it - hours * 60;
                return (hours !== 0 ? `${hours}:` : '') + ((minutes < 10 && hours !== 0) ? `0${minutes}` : `${minutes}`);
            });
        }

        get minutesBetweenNextLast(): Option<number> {
            const nextStartTime: Option<Date> = liftA2(option)(curry(SchoolBusService.startTimeInCampus))(this.nextByFromTo)(this.fromCampus).getOrElse(none);
            const lastStartTime: Option<Date> = liftA2(option)(curry(SchoolBusService.startTimeInCampus))(this.lastByFromTo)(this.fromCampus).getOrElse(none);
            return liftA2(option)(fpDifferenceInMinutes)(lastStartTime)(nextStartTime) as Option<number>;
        }

        get currentWaitingPercentage(): Option<number> {
            return liftA2(option)(curry(toPercent))(this.minutesToNext)(this.minutesBetweenNextLast);
        }

        get current() {
            if (this.semesterForDate(this.now).isNone()) {
                this.fetchSemester({forDate: this.now});
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
    }
</script>
