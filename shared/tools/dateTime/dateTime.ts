import * as dateNormalizer from "date-normalizer";

export namespace DateTimeService {
    export const normalizeDateTimeInObject = (dateNormalizer as any)['date-normalizer'].normalizeDateInObject;

    /**
     * 合并日期和时间，合并结果有 @param date 的日期 和 @param time 的时间
     */
    export function mergeDateTime(date: Date, time: Date): Date {
        return new Date(date.getFullYear(), date.getMonth(), date.getDate(), time.getHours(), time.getMinutes(), time.getSeconds());
    }

    export function now(): Date {
        return new Date();
    }
}