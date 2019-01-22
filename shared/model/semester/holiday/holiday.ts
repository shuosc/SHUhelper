import {DateRange} from "../../dateRange/dateRange";
import {Shift} from "./shift/shift";
import {HolidayWithShift} from "./holiday";

export interface Holiday extends DateRange {
    readonly name: string;
}

export interface HolidayWithShift extends Holiday {
    readonly shifts: Array<Shift>;
}

export namespace HolidayService {
    export function hasShift(holiday: Holiday): holiday is HolidayWithShift {
        return 'shifts' in holiday;
    }
}
