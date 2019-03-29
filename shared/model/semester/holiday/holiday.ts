import {Shift} from "./shift/shift";
import {HolidayWithShift} from "./holiday";
import {Interval} from "date-fns"

export interface Holiday extends Interval {
    readonly start: Date;
    readonly end: Date;
    readonly name: string;
}

export interface HolidayWithShift extends Holiday {
    readonly shifts: Array<Shift>;
}

export function hasShift(holiday: Holiday): holiday is HolidayWithShift {
    return 'shifts' in holiday;
}
