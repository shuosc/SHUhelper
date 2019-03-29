import {hasShift, Holiday} from "../../shared/model/semester/holiday/holiday";
import {Option} from "fp-ts/lib/Option";
import {findFirst, findIndex} from "fp-ts/lib/Array";
import {Semester} from "../../shared/model/semester/semester";
import {SectorRepository, SectorService} from "./sector.service";
import {addDays, eachWeekOfInterval, getDay, Interval, isAfter, isBefore, isSameDay, isWithinInterval} from "date-fns"
import {partial} from "~/tools/partial";
import {extractTime} from "~/tools/dateTime";

export const HOLIDAY = 7;

export interface DateTimeInSemester {
    dateTime: Date;
    semester: Semester;
}

export namespace DateTimeInSemesterService {
    function getWeeks(semester: Semester): Array<Interval> {
        return eachWeekOfInterval(semester).map(firstDayOfWeek => {
            return {start: firstDayOfWeek, end: addDays(firstDayOfWeek, 7)};
        });
    }

    function getWorkingWeeks(semester: Semester): Array<Interval> {
        return getWeeks(semester).filter(week => {
            const monday = {semester: semester, dateTime: addDays(week.start, 1)};
            const friday = {semester: semester, dateTime: addDays(week.start, 5)};
            const isMondayHoliday = isHoliday(monday);
            const isFridayHoliday = isHoliday(friday);
            return !isMondayHoliday && !isFridayHoliday;
        });
    }

    export function schoolDay(dateTime: DateTimeInSemester): number {
        for (const holiday of dateTime.semester.holidays) {
            if (hasShift(holiday)) {
                for (const shift of holiday.shifts) {
                    if (isSameDay(dateTime.dateTime, shift.from)) {
                        return HOLIDAY;
                    } else if (isSameDay(shift.to, dateTime.dateTime)) {
                        return getDay(shift.from);
                    }
                }
                if (isWithinInterval(dateTime.dateTime, holiday)) {
                    return HOLIDAY;
                }
            } else if (isWithinInterval(dateTime.dateTime, holiday)) {
                return HOLIDAY;
            }
        }
        return getDay(dateTime.dateTime);
    }

    export function getHoliday(dateTime: DateTimeInSemester): Option<Holiday> {
        return findFirst(dateTime.semester.holidays, partial(isWithinInterval, dateTime.dateTime));
    }

    export function getNextHoliday(dateTime: DateTimeInSemester): Option<Holiday> {
        return findFirst(dateTime.semester.holidays, it => isAfter(it.start, dateTime.dateTime));
    }

    export function isHoliday(dateTime: DateTimeInSemester): boolean {
        return schoolDay(dateTime) === HOLIDAY;
    }

    export function isWorkingDay(dateTime: DateTimeInSemester): boolean {
        return schoolDay(dateTime) !== 0 && schoolDay(dateTime) !== 6 && schoolDay(dateTime) !== HOLIDAY;
    }

    /**
     * 这是第几周
     * 如果这天放假，返回0
     */
    export function getWorkWeekIndex(dateTime: DateTimeInSemester): number {
        if (isHoliday(dateTime)) {
            return 0;
        }
        return findIndex(getWorkingWeeks(dateTime.semester), week => {
            return isWithinInterval(dateTime.dateTime, week);
        }).map(it => it + 1).getOrElse(0);
    }


    /**
     * 判断某个时间点是否在第一节课之前
     */
    export function isBeforeFirstSector(dateTime: DateTimeInSemester): boolean {
        return isBefore(extractTime(dateTime.dateTime), SectorRepository.sectors.head.start);
    }

    /**
     * 判断某个时间点是否在最后一节课之后
     */
    export function isAfterLastSector(dateTime: DateTimeInSemester): boolean {
        return isAfter(extractTime(dateTime.dateTime), SectorRepository.sectors.last().end);
    }

    /**
     * 找出某一时间点的下一节课
     */
    export function nextSectorIndex(dateTime: DateTimeInSemester): Option<number> {
        return SectorRepository.sectors.findIndex(it => isAfter(it.start, extractTime(dateTime.dateTime)));
    }

    export function nextSector(dateTime: DateTimeInSemester): Option<Interval> {
        return this.nextSectorIndex.chain(index => SectorRepository.sectors.lookup(index));
    }

    /**
     * 找出某一时间点的上一节课
     */
    export function lastSectorIndex(dateTime: DateTimeInSemester): Option<number> {
        return SectorRepository.sectors.findLastIndex(it => isBefore(it.end, extractTime(dateTime.dateTime)));
    }

    export function lastSector(dateTime: DateTimeInSemester): Option<Interval> {
        return lastSectorIndex(dateTime).chain(index => SectorRepository.sectors.lookup(index));
    }

    /**
     * 找出某一时间点的这一节课
     */
    export function currentSectorIndex(dateTime: DateTimeInSemester): Option<number> {
        return SectorService.sectorIndexForTime(dateTime.dateTime);
    }

    export function currentSector(dateTime: DateTimeInSemester): Option<Interval> {
        return currentSectorIndex(dateTime).chain(index => SectorRepository.sectors.lookup(index));
    }

    /**
     * 找出现在正在进行的课间休息时间
     */
    export function currentRest(dateTime: DateTimeInSemester): Option<Interval> {
        return SectorRepository.rests.findFirst(it => isWithinInterval(extractTime(dateTime.dateTime), it));
    }
}
