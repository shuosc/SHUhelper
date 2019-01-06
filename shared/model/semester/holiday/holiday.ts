import {DateRange, DateRangeJson, DateRangeService} from "../../dateRange/dateRange";

export interface Holiday extends DateRange {
    readonly name: string;
}

export interface HolidayJson extends DateRangeJson {
    readonly name: string;
}

export namespace HolidayService {
    export function normalize(json: HolidayJson): Holiday {
        return {
            name: json.name,
            ...DateRangeService.normalize(json)
        }
    }
}