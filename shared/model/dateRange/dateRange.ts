import {Maybe} from "../../tools/functools/maybe";
import {TimeService} from "../../tools/time/time";

/**
 * 日期区间类型
 */
export interface DateRange {
    readonly begin: Date;
    readonly end: Date;
}

export namespace DateRangeService {
    export function isDateIn(dateRange: DateRange, date: Date): boolean {
        return dateRange.begin <= date && date < dateRange.end;
    }

    export function nearestToDate<T extends DateRange>(dateRanges: Array<T>, date: Date): Maybe<T> {
        const result = dateRanges
            .sort((first: DateRange, second: DateRange) => {
                return first.begin.getTime() - second.begin.getTime();
            })
            .find((it: DateRange) => it.begin > date);
        return new Maybe(result);
    }

    export function daysTo(date: Date, dateRange: DateRange): number {
        if (isDateIn(dateRange, date)) {
            return 0;
        }
        if (date < dateRange.begin) {
            return TimeService.timestampDifferenceToDay(dateRange.begin.getTime() - date.getTime());
        } else if (date >= dateRange.begin) {
            return TimeService.timestampDifferenceToDay(date.getTime() - dateRange.end.getTime());
        }
        throw Error("Should never reach here")
    }
}