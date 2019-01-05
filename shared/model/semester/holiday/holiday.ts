import {DateRange} from "../../dateRange/dateRange";

export interface Holiday extends DateRange {
    readonly name: string;
}
