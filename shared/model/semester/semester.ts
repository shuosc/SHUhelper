import {DateRange, DateRangeJson, DateRangeService} from "../dateRange/dateRange";
import {Holiday, HolidayJson, HolidayService} from "./holiday/holiday";
import {assert} from "../../tools/assert";
import {DAY_CHINESE_TO_NUMBER} from "../../tools/date";

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
    export function getSchoolDayInSemester(semester: Semester, date: Date): number {
        assert(DateRangeService.isDateIn(semester, date));
        for (const holiday of semester.holidays) {
            if (DateRangeService.isDateIn(holiday, date)) {
                return DAY_CHINESE_TO_NUMBER.get('日') as number;
            }
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
}