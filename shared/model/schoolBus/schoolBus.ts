import {Campus, CampusRepository} from "../campus/campus";
import {find, findIndex, just, Maybe} from "../../tools/functools/maybe";
import {assert} from "../../tools/assert";
import * as _ from "lodash";
import {TimeService} from "../../tools/dateTime/time/time";
// Silly WebStorm knows nothing about import a json!
// @ts-ignore
import * as schedule from "./shedule.json";
import {Semester, SemesterService} from "../semester/semester";

export type SchoolBus = Array<{ campusId: number, startTime?: Date }>

export namespace SchoolBusService {
    export function hasFromTo(bus: SchoolBus, from: Campus, to: Campus): Boolean {
        assert(from !== to);
        const fromIndex = bus.findIndex((it) => it.campusId === from.id);
        const toIndex = bus.findIndex((it) => it.campusId === to.id);
        return fromIndex !== -1 && toIndex !== -1 && fromIndex < toIndex;
    }

    export function startTimeInCampus(bus: SchoolBus, campus: Campus): Maybe<Date> {
        return find(bus, it => it.campusId === campus.id).flatMap(it => just(it.startTime));
    }
}

export enum SchoolBusRoutineType {
    WorkingDay = 0,
    NonWorkingDay = 1,
    SummerHoliday = 2
}

export namespace SchoolBusRepository {
    function parseRoutine(json: any): Array<SchoolBus> {
        const result = [];
        for (let route in json) {
            const campuses = route.split('-')
                .map(CampusRepository.getByName)
                .map(it => it.value);
            for (let routins of json[route]) {
                const times: Array<Date | undefined> = routins.map(TimeService.createTimeFromString).map((it: Maybe<Date>) => it.value);
                times.push(undefined);
                assert(campuses.length === times.length);
                result.push(_.zip(campuses, times)
                    .map(it => {
                        if (it[1] === undefined) {
                            return {
                                campusId: (it[0] as Campus).id
                            }
                        } else {
                            return {
                                campusId: (it[0] as Campus).id,
                                startTime: it[1]
                            }
                        }
                    }));
            }
        }
        return result;
    }

    function parseJson(): Array<Array<SchoolBus>> {
        return [
            parseRoutine(schedule["工作日"]),
            parseRoutine(schedule["休息日"])
        ];
    }

    export const routines: Array<Array<SchoolBus>> = parseJson();

    export function getByFromTo(from: Campus, to: Campus, type: SchoolBusRoutineType): Array<SchoolBus> {
        const routinesForThisType = routines[type as number];
        return routinesForThisType.filter(_.partial(SchoolBusService.hasFromTo, _, from, to))
            .sort((a: SchoolBus, b: SchoolBus) => {
                const aStartTime = SchoolBusService.startTimeInCampus(a, from);
                const bStartTime = SchoolBusService.startTimeInCampus(b, from);
                assert(!aStartTime.isNull && !bStartTime.isNull);
                return (aStartTime.value as Date).getTime() - (bStartTime.value as Date).getTime();
            });
    }

    function getByFromToAtTime(from: Campus, to: Campus, time: Date, type: SchoolBusRoutineType): Maybe<SchoolBus> {
        const routinesWithRightFromTo = getByFromTo(from, to, type);
        return find(routinesWithRightFromTo, (bus: SchoolBus) => {
            const fromStartTime = SchoolBusService.startTimeInCampus(bus, from);
            assert(!fromStartTime.isNull);
            return TimeService.earlierThan(time, fromStartTime.value as Date);
        });
    }

    export function getByFromToAtDateTime(from: Campus, to: Campus, dateTime: Date, semester: Semester): Maybe<SchoolBus> {
        let isWorkingDay = SemesterService.isWorkingDay(semester, dateTime);
        if (isWorkingDay) {
            return getByFromToAtTime(from, to, dateTime, SchoolBusRoutineType.WorkingDay);
        } else {
            return getByFromToAtTime(from, to, dateTime, SchoolBusRoutineType.NonWorkingDay);
        }
    }

    function getLastByFromToAtTime(from: Campus, to: Campus, time: Date, type: SchoolBusRoutineType): Maybe<SchoolBus> {
        const routinesWithRightFromTo = getByFromTo(from, to, type);
        const index: Maybe<number> = findIndex(routinesWithRightFromTo, (bus: SchoolBus) => {
            const fromStartTime = SchoolBusService.startTimeInCampus(bus, from);
            assert(!fromStartTime.isNull);
            return TimeService.earlierThan(time, fromStartTime.value as Date);
        }).flatMap(it => it - 1 < 0 ? new Maybe<number>(null) : just(it - 1));
        return index.map(it => routinesWithRightFromTo[it]);
    }

    export function getLastByFromToAtDateTime(from: Campus, to: Campus, dateTime: Date, semester: Semester): Maybe<SchoolBus> {
        let isWorkingDay = SemesterService.isWorkingDay(semester, dateTime);
        if (isWorkingDay) {
            return getLastByFromToAtTime(from, to, dateTime, SchoolBusRoutineType.WorkingDay);
        } else {
            return getLastByFromToAtTime(from, to, dateTime, SchoolBusRoutineType.NonWorkingDay);
        }
    }
}
