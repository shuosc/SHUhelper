import {DateRange} from "../dateRange/dateRange";
import {Holiday} from "./holiday/holiday";

export interface Semester extends DateRange {
    readonly _id: any;
    readonly name: string;
    readonly holidays: Array<Holiday>;
}