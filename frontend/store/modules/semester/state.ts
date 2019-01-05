import {DateRange} from "../../../../shared/model/dateRange/dateRange";
import {Holiday} from "../../../../shared/model/semester/holiday/holiday";

export interface Semester {
    _id: any;
    name: string;
    dateRange: DateRange;
    holidays: Array<Holiday>;
}

export interface State {
    semesters: Array<Semester> | null;
}

export const state = (): State => ({
    semesters: null
});