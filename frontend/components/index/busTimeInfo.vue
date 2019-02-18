<template>
    <v-card class="pa-0">
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
                            <v-flex v-if="!timestampDifferenceToNextBus.isNull" xs12>
                                <v-layout align-center class="mb-2" row wrap>
                                    <v-flex sm1 v-if="!timestampDifferenceLastToNextBus.isNull" xs2>
                                        <v-progress-circular
                                                :size="35"
                                                :value="toPercent(timestampDifferenceToNextBus.value,timestampDifferenceLastToNextBus.value)"
                                                :width="2"
                                                color="green">
                                            {{timestampDifferenceToNextBus.map(timestampDifferenceToHourMinutesString).value}}
                                        </v-progress-circular>
                                    </v-flex>
                                    <v-flex sm11 xs10>
                                        此线路下一班校车还有{{timestampDifferenceToNextBus.map(timestampDifferenceToHourMinutesChinese).value}}
                                    </v-flex>
                                </v-layout>
                            </v-flex>
                            <v-flex v-else xs12>
                                今天此线路最后一辆校车已经走了哦,下次请早点来吧！
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
                                                :items="timeTable.map((it,index) => {return {index:index+1,time:it.toTimeString().slice(0,5)}})"
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
    import {avatarSize} from "~/tools/avatarSize";
    import Component, {namespace} from "nuxt-class-component";
    import {Vue, Watch} from 'vue-property-decorator';
    import {Campus, CampusRepository} from "../../../shared/model/campus/campus";
    import {
        SchoolBusRepository,
        SchoolBusRoutine,
        SchoolBusRoutineType,
        SchoolBusService
    } from "../../../shared/model/schoolBus/schoolBus"
    import * as semesterModule from '~/store/modules/semester';
    import {just, Maybe} from "../../../shared/tools/functools/maybe";
    import {Semester} from "../../../shared/model/semester/semester";
    import {TimeService} from "../../../shared/tools/dateTime/time/time";
    import {toPercent} from "~/tools/toPercent";
    import * as _ from "lodash";
    import timestampDifferenceToHourMinutesString = TimeService.timestampDifferenceToHourMinutesString;
    import timestampDifferenceToHourMinutesChinese = TimeService.timestampDifferenceToHourMinutesChinese;

    const SemesterNamespace = namespace(semesterModule.name);

    @Component({
        methods: {
            avatarSize,
            toPercent,
            timestampDifferenceToHourMinutesString,
            timestampDifferenceToHourMinutesChinese
        }
    })
    export default class BusTimeInfo extends Vue {
        SchoolBusRoutineType = SchoolBusRoutineType;
        SchoolBusRepository = SchoolBusRepository;
        CampusRepository = CampusRepository;
        now = new Date();
        schoolBusRoutineType = SchoolBusRoutineType.WorkingDay;
        fromCampusId: number = 0;
        toCampusId: number = 1;
        expanded = [false];
        @SemesterNamespace.Getter getSemesterForDate!: (date: Date) => Maybe<Semester>;

        mounted() {
            setInterval(() => {
                this.now = new Date()
            }, 1000);
        }

        get timeTable(): Array<Date> {
            const fromCampus = CampusRepository.getById(this.fromCampusId).value as Campus;
            const toCampus = CampusRepository.getById(this.toCampusId).value as Campus;
            return SchoolBusRepository.getByFromTo(fromCampus, toCampus, this.schoolBusRoutineType)
                .map((schoolBus: SchoolBusRoutine) => SchoolBusService.startTimeInCampus(schoolBus, fromCampus).value as Date);
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

        get timestampDifferenceToNextBus(): Maybe<number> {
            const fromCampus = CampusRepository.getById(this.fromCampusId);
            const toCampus = CampusRepository.getById(this.toCampusId);
            const currentSemester = this.getSemesterForDate(this.now);
            // noinspection TypeScriptValidateTypes
            return just(_.curry(SchoolBusRepository.timeDifferenceToNext))
                .apply(fromCampus)
                .apply(toCampus)
                .apply(just(this.now))
                .apply(currentSemester);
        }

        get timestampDifferenceLastToNextBus(): Maybe<number> {
            const fromCampus = CampusRepository.getById(this.fromCampusId);
            const toCampus = CampusRepository.getById(this.toCampusId);
            const currentSemester = this.getSemesterForDate(this.now);
            // noinspection TypeScriptValidateTypes
            return just(_.curry(SchoolBusRepository.timeDifferenceBetweenLastAndNext))
                .apply(fromCampus)
                .apply(toCampus)
                .apply(just(this.now))
                .apply(currentSemester);
        }
    }
</script>
