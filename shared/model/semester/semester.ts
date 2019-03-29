import {Holiday} from "./holiday/holiday";
import {Interval} from "date-fns";

export interface Semester extends Interval {
    readonly start: Date;
    readonly end: Date;
    readonly _id: any;
    readonly name: string;
    readonly holidays: Array<Holiday>;
    readonly courseSelectionPort8080: boolean;
}

