import {DateRange, DateRangeService} from "../dateRange/dateRange";
import {Holiday, HolidayService, HolidayWithShift} from "./holiday/holiday";
import {assert} from "../../tools/assert";
import {find, Maybe} from "../../tools/functools/maybe";
import {clone} from "../../tools/clone";
import {DateService} from "../../tools/dateTime/date/date";
import * as _ from "lodash";

export interface Semester extends DateRange {
    readonly _id: any;
    readonly name: string;
    readonly holidays: Array<Holiday | HolidayWithShift>;
}

export namespace SemesterService {
    export const HOLIDAY = 7;

    /**
     * 返回某一天上哪天的课
     * @return 如果是调休补上班日，返回补的那一天星期几
     *         如果是假期，返回 HOLIDAY
     *         否则是星期几就返回星期几
     */
    export function getSchoolDay(semester: Semester, date: Date): number {
        assert(DateRangeService.isDateIn(semester, date));
        for (const holiday of semester.holidays) {
            if (HolidayService.hasShift(holiday)) {
                for (const shift of holiday.shifts) {
                    if (DateService.isSameDate(date, shift.from)) {
                        return HOLIDAY;
                    } else if (DateService.isSameDate(date, shift.to)) {
                        return shift.from.getDay();
                    }
                }
                if (DateRangeService.isDateIn(holiday, date)) {
                    return HOLIDAY;
                }
            } else if (DateRangeService.isDateIn(holiday, date)) {
                return HOLIDAY;
            }
        }
        return date.getDay();
    }

    export function isHoliday(semester: Semester, date: Date): boolean {
        return getSchoolDay(semester, date) === HOLIDAY;
    }

    export function getHolidayForDate(semester: Semester, date: Date): Maybe<Holiday | HolidayWithShift> {
        const isDateIn = _.partial(DateRangeService.isDateIn, _, date);
        return find<Holiday | HolidayWithShift>(semester.holidays, isDateIn);
    }

    function getShiftFrom(semester: Semester, date: Date): Date {
        const result = find(semester.holidays.filter(HolidayService.hasShift), holiday => DateRangeService.isDateIn(holiday, date))
            .flatMap(theHoliday => find(theHoliday.shifts, shift => DateService.isSameDate(date, shift.to)))
            .map(theShift => theShift.from);
        return result.value === null ? date : result.value;
    }

    /**
     * 获取某一天是学期中的第几周
     * 假期不算，返回0
     */
    export function getWeekIndex(semester: Semester, date: Date): number {
        assert(semester.begin.getDay() === 1);
        if (isHoliday(semester, date)) {
            return 0;
        }
        let currentMonday = semester.begin;
        const dateToFind = getShiftFrom(semester, date);
        for (let i = 1; i <= 12; ++i) {
            const currentFriday = new Date(currentMonday.getFullYear(), currentMonday.getMonth(), currentMonday.getDate() + 5);
            while (isHoliday(semester, currentMonday) && isHoliday(semester, currentFriday)) {
                currentMonday = DateService.toNextWeek(currentMonday);
            }
            const nextMonday = DateService.toNextWeek(currentMonday);
            if (nextMonday > dateToFind) {
                return i;
            }
            currentMonday = nextMonday;
        }
        throw Error("Should never reached here")
    }

    /**
     * 获取从@arg from 开始到 @arg to 的工作日数量
     */
    export function getWorkingDayCount(semester: Semester, from: Date, to: Date): number {
        let result = 0;
        for (let day = clone(from); !DateService.isSameDate(day, to); day.setDate(day.getDate() + 1)) {
            if (!(isHoliday(semester, day) || day.getDay() === 0 || day.getDay() === 6)) {
                ++result;
            }
        }
        return result;
    }

    /**
     * 获取总的工作日数量
     */
    export function getTotalWorkingDayCount(semester: Semester): number {
        return getWorkingDayCount(semester, semester.begin, semester.end);
    }
}