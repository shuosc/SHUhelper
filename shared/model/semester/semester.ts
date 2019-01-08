import {DateRange, DateRangeJson, DateRangeService} from "../dateRange/dateRange";
import {Holiday, HolidayJson, HolidayService} from "./holiday/holiday";
import {assert} from "../../tools/assert";
import {DAY_CHINESE_TO_NUMBER, toNextWeek} from "../../tools/date";

export interface Semester extends DateRange {
    readonly _id: any;
    readonly name: string;
    readonly holidays: Array<Holiday>;
}

export interface SemesterJson extends DateRangeJson {
    readonly _id: any;
    readonly name: string;
    readonly holidays: Array<HolidayJson>;
}

export namespace SemesterService {
    export function isHoliday(semester: Semester, date: Date) {
        for (const holiday of semester.holidays) {
            if (DateRangeService.isDateIn(holiday, date)) {
                return true;
            }
        }
        return false;
    }

    export function getSchoolDayInSemester(semester: Semester, date: Date): number {
        assert(DateRangeService.isDateIn(semester, date));
        if (isHoliday(semester, date)) {
            return DAY_CHINESE_TO_NUMBER.get('日') as number;
        }
        return date.getDay();
    }

    export function normalize(json: SemesterJson): Semester {
        return {
            _id: json._id,
            name: json.name,
            holidays: json.holidays.map(it => HolidayService.normalize(it)),
            ...DateRangeService.normalize(json)
        };
    }

    export function getWeekIndex(semester: Semester, date: Date): number {
        assert(semester.begin.getDay() === 1);
        if (isHoliday(semester, date)) {
            return 0;
        }
        let currentFirstDayOfWeek = semester.begin;
        for (let i = 1; i <= 10; ++i) {
            while (isHoliday(semester, currentFirstDayOfWeek)) {
                currentFirstDayOfWeek = toNextWeek(currentFirstDayOfWeek);
            }
            const nextFirstDay = toNextWeek(currentFirstDayOfWeek);
            if (nextFirstDay > date) {
                return i;
            }
            currentFirstDayOfWeek = nextFirstDay;
        }
        return -1;
    }
}