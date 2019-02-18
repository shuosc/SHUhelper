import {Campus, CampusRepository} from "../campus/campus";
import {just, Maybe} from "../../tools/functools/maybe";
import {assert} from "../../tools/assert";
import * as _ from "lodash";
import {TimeService} from "../../tools/dateTime/time/time";
// Silly WebStorm knows nothing about import a json!
// @ts-ignore
import * as schedule from "./shedule.json";
import {Semester, SemesterService} from "../semester/semester";
import {find, findBefore} from "../../tools/functools/array/array";

interface SchoolBusStation {
    campusId: number,
    startTime?: Date
}

export type SchoolBusRoutine = Array<SchoolBusStation>;

export namespace SchoolBusService {
    export function hasFromTo(bus: SchoolBusRoutine, from: Campus, to: Campus): boolean {
        assert(from !== to);
        const fromIndex = bus.findIndex(it => it.campusId === from.id);
        const toIndex = bus.findIndex(it => it.campusId === to.id);
        return fromIndex !== -1 && toIndex !== -1 && fromIndex < toIndex;
    }

    export function startTimeInCampus(bus: SchoolBusRoutine, campus: Campus): Maybe<Date> {
        return find(bus, it => it.campusId === campus.id).flatMap(it => just(it.startTime));
    }
}

export enum SchoolBusRoutineType {
    WorkingDay = 0,
    NonWorkingDay = 1,
    SummerHoliday = 2
}

export namespace SchoolBusRepository {
    function parseSchoolBusStation(campusId: number, startTime: Date | undefined): SchoolBusStation {
        if (startTime === undefined) {
            return {
                campusId: campusId
            }
        } else {
            return {
                campusId: campusId,
                startTime: startTime
            }
        }
    }

    function parseRoutineForOneType(json: any): Array<SchoolBusRoutine> {
        const result = [];
        for (let route in json) {
            const campuses = route.split('-')
                .map(CampusRepository.getByName)
                .map(it => (it.value as Campus).id);
            for (let routines of json[route]) {
                const times: Array<Date | undefined> = routines
                    .map(TimeService.createTimeFromHourMinuteString)
                    .map((it: Maybe<Date>) => it.value);
                result.push(_.zip(campuses, times).map(it => parseSchoolBusStation(it[0] as number, it[1])));
            }
        }
        return result;
    }

    function parseJson(): Array<Array<SchoolBusRoutine>> {
        return [
            parseRoutineForOneType(schedule["工作日"]),
            parseRoutineForOneType(schedule["休息日"])
        ];
    }

    export const routines: Array<Array<SchoolBusRoutine>> = parseJson();

    /**
     * 获取从 @arg type 下 从@arg from 到 @arg to 的所有车次
     */
    export function getByFromTo(from: Campus, to: Campus, type: SchoolBusRoutineType): Array<SchoolBusRoutine> {
        const routinesForThisType = routines[type as number];
        return routinesForThisType.filter(_.partial(SchoolBusService.hasFromTo, _, from, to))
            .sort((a: SchoolBusRoutine, b: SchoolBusRoutine) => {
                const aStartTime = SchoolBusService.startTimeInCampus(a, from);
                const bStartTime = SchoolBusService.startTimeInCampus(b, from);
                assert(!aStartTime.isNull && !bStartTime.isNull);
                return (aStartTime.value as Date).getTime() - (bStartTime.value as Date).getTime();
            });
    }

    type FindFunction = (routines: Array<SchoolBusRoutine>, pred: (bus: SchoolBusRoutine) => boolean) => Maybe<SchoolBusRoutine>

    function findByFromToAtTime(findFunction: FindFunction, from: Campus, to: Campus, time: Date, type: SchoolBusRoutineType) {
        const routinesWithRightFromTo = getByFromTo(from, to, type);
        return findFunction(routinesWithRightFromTo, (bus: SchoolBusRoutine) => {
            const fromStartTime = SchoolBusService.startTimeInCampus(bus, from);
            assert(!fromStartTime.isNull);
            return TimeService.earlierThan(time, fromStartTime.value as Date);
        });
    }

    function getNextByFromToAtTime(from: Campus, to: Campus, time: Date, type: SchoolBusRoutineType): Maybe<SchoolBusRoutine> {
        return findByFromToAtTime(find, from, to, time, type);
    }

    /**
     * 获取 @arg dateTime 时下一班从 @arg from 到 @arg to 的车次
     */
    export function getNextByFromTo(from: Campus, to: Campus, dateTime: Date, semester: Semester): Maybe<SchoolBusRoutine> {
        let isWorkingDay = SemesterService.isWorkingDay(semester, dateTime);
        if (isWorkingDay) {
            return getNextByFromToAtTime(from, to, dateTime, SchoolBusRoutineType.WorkingDay);
        } else {
            return getNextByFromToAtTime(from, to, dateTime, SchoolBusRoutineType.NonWorkingDay);
        }
    }

    function getLastByFromToAtTime(from: Campus, to: Campus, time: Date, type: SchoolBusRoutineType): Maybe<SchoolBusRoutine> {
        return findByFromToAtTime(findBefore, from, to, time, type);
    }

    /**
     * 获取 @arg dateTime 时上一班从 @arg from 到 @arg to 的车次
     */
    export function getLastByFromTo(from: Campus, to: Campus, dateTime: Date, semester: Semester): Maybe<SchoolBusRoutine> {
        let isWorkingDay = SemesterService.isWorkingDay(semester, dateTime);
        if (isWorkingDay) {
            return getLastByFromToAtTime(from, to, dateTime, SchoolBusRoutineType.WorkingDay);
        } else {
            return getLastByFromToAtTime(from, to, dateTime, SchoolBusRoutineType.NonWorkingDay);
        }
    }

    export function timeDifferenceToNext(from: Campus, to: Campus, dateTime: Date, semester: Semester): Maybe<number> {
        const startTimeInCampus = _.partial(SchoolBusService.startTimeInCampus, _, from);
        const nextStartTime = getNextByFromTo(from, to, dateTime, semester).flatMap(startTimeInCampus);
        return nextStartTime.map(_.partial(TimeService.timeDistance, dateTime) as any)
    }

    /**
     *
     * 获取 @arg dateTime 时上一班从 @arg from 到 @arg to 的车次到下一班从 @arg from 到 @arg to 的车次之间的时间差
     * 以毫秒为单位表示
     */
    export function timeDifferenceBetweenLastAndNext(from: Campus, to: Campus, dateTime: Date, semester: Semester): Maybe<number> {
        const startTimeInCampus = _.partial(SchoolBusService.startTimeInCampus, _, from);
        const lastStartTime = getLastByFromTo(from, to, dateTime, semester).flatMap(startTimeInCampus);
        const nextStartTime = getNextByFromTo(from, to, dateTime, semester).flatMap(startTimeInCampus);
        return just(_.curry(TimeService.timeDistance)).apply(lastStartTime).apply(nextStartTime);
    }
}
