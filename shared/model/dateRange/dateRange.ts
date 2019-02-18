import {Maybe} from "../../tools/functools/maybe";
import {TimeService} from "../../tools/dateTime/time/time";
import {find} from "../../tools/functools/array/array";

/**
 * 日期区间类型
 */
export interface DateRange {
    readonly begin: Date;
    readonly end: Date;
}

export namespace DateRangeService {
    /**
     * 判断 @arg date 是否在 @arg dateRange 之中
     */
    export function isDateIn(dateRange: DateRange, date: Date): boolean {
        return dateRange.begin <= date && date < dateRange.end;
    }

    /**
     * 求 @arg dateRanges 之中，开始在 @arg date 之后的中的最先的一个
     */
    export function nextFromDate<T extends DateRange>(dateRanges: Array<T>, date: Date): Maybe<T> {
        return find(dateRanges
            .sort((first: DateRange, second: DateRange) => {
                return first.begin.getTime() - second.begin.getTime();
            }), (it: T) => it.begin > date);
    }

    /**
     * 返回 @arg date 距离 @arg dateRange 的天数
     */
    export function daysTo(date: Date, dateRange: DateRange): number {
        if (isDateIn(dateRange, date)) {
            return 0;
        }
        if (date < dateRange.begin) {
            return TimeService.timestampDifferenceToDay(dateRange.begin.getTime() - date.getTime());
        } else if (date >= dateRange.end) {
            return TimeService.timestampDifferenceToDay(date.getTime() - dateRange.end.getTime());
        }
        throw Error("Should never reach here")
    }
}