// Silly WebStorm knows nothing about import a json!
// @ts-ignore
import * as schedule from "~/static/shedule.json";
import {findFirst, findLast, zip} from "fp-ts/lib/Array";
import {Option} from "fp-ts/lib/Option";
import {DateTimeInSemester, DateTimeInSemesterService} from "~/service/dateTimeInSemester.service";
import {CampusRepository} from "~/repository/campus.repository";
import {Campus} from "../../shared/model/campus/campus";
import {SchoolBusRoutine, SchoolBusRoutineType, SchoolBusStation} from "../../shared/model/schoolBus/schoolBus";
import {SchoolBusService} from "~/service/schoolBus";
import {isAfter, isBefore, parse} from "date-fns";
import {createDate} from "../../backend/tools/dateTime";
import {_, partial} from "~/tools/partial";
import {assert} from "~/tools/assert";

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
                .map(it => it.toNullable().id);
            for (let routines of json[route]) {
                const times: Array<Date | null> = routines.map(it => parse(it, "HH:mm", createDate(0, 0, 0)));
                times.push(undefined);
                result.push(zip(campuses, times).map(it => parseSchoolBusStation(it[0] as number, it[1])));
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
        return routinesForThisType.filter(partial(SchoolBusService.hasFromTo, _, from, to))
            .sort((a: SchoolBusRoutine, b: SchoolBusRoutine) => {
                const aStartTime = SchoolBusService.startTimeInCampus(a, from);
                const bStartTime = SchoolBusService.startTimeInCampus(b, from);
                assert(aStartTime.isSome() && bStartTime.isSome());
                return aStartTime.toNullable().getTime() - bStartTime.toNullable().getTime();
            });
    }

    function getNextByFromToAtTime(from: Campus, to: Campus, time: Date, type: SchoolBusRoutineType): Option<SchoolBusRoutine> {
        const routinesWithRightFromTo = getByFromTo(from, to, type);
        return findFirst(routinesWithRightFromTo, (bus: SchoolBusRoutine) => {
            const fromStartTime = SchoolBusService.startTimeInCampus(bus, from);
            assert(fromStartTime.isSome());
            return isBefore(time, fromStartTime.toNullable());
        });
    }

    /**
     * 获取 @arg dateTime 时下一班从 @arg from 到 @arg to 的车次
     */
    export function getNextByFromTo(from: Campus, to: Campus, dateTime: DateTimeInSemester): Option<SchoolBusRoutine> {
        let isWorkingDay = DateTimeInSemesterService.isWorkingDay(dateTime);
        if (isWorkingDay) {
            return getNextByFromToAtTime(from, to, dateTime.dateTime, SchoolBusRoutineType.WorkingDay);
        } else {
            return getNextByFromToAtTime(from, to, dateTime.dateTime, SchoolBusRoutineType.NonWorkingDay);
        }
    }

    function getLastByFromToAtTime(from: Campus, to: Campus, time: Date, type: SchoolBusRoutineType): Option<SchoolBusRoutine> {
        const routinesWithRightFromTo = getByFromTo(from, to, type);
        return findLast(routinesWithRightFromTo, (bus: SchoolBusRoutine) => {
            const fromStartTime = SchoolBusService.startTimeInCampus(bus, from);
            assert(fromStartTime.isSome());
            return isAfter(time, fromStartTime.toNullable());
        });
    }

    /**
     * 获取 @arg dateTime 时上一班从 @arg from 到 @arg to 的车次
     */
    export function getLastByFromTo(from: Campus, to: Campus, dateTime: DateTimeInSemester): Option<SchoolBusRoutine> {
        let isWorkingDay = DateTimeInSemesterService.isWorkingDay(dateTime);
        if (isWorkingDay) {
            return getLastByFromToAtTime(from, to, dateTime.dateTime, SchoolBusRoutineType.WorkingDay);
        } else {
            return getLastByFromToAtTime(from, to, dateTime.dateTime, SchoolBusRoutineType.NonWorkingDay);
        }
    }
}
