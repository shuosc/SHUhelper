import {DateRange} from "../../../../shared/model/dateRange";
import {Holiday} from "../../../../shared/model/holiday";

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