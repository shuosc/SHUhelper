import {Maybe} from "../functools/maybe";
import {get} from "../functools/get";

const DAY_CHINESE_TO_NUMBER = new Map<string, number>(
    [
        ['日', 0],
        ['一', 1],
        ['二', 2],
        ['三', 3],
        ['四', 4],
        ['五', 5],
        ['六', 6]
    ]
);

export function dayChineseToNumber(chinese: string): Maybe<number> {
    return get(DAY_CHINESE_TO_NUMBER, chinese);
}

export const DAY_NUMBER_TO_CHINESE = ['日', '一', '二', '三', '四', '五', '六'];


/**
 * 合并日期和时间，合并结果有 @param date 的日期 和 @param time 的时间
 */
export function mergeDateTime(date: Date, time: Date) {
    return new Date(date.getFullYear(), date.getMonth(), date.getDate(), time.getHours(), time.getMinutes(), time.getSeconds());
}

export namespace DateService {
    /**
     * 使用人类的格式创建一个日期对象
     * @param year 年份
     * @param month 月份
     * @param day 日期
     * JS's Date is a piece of sh*t, month has to minus 1 but others doesn't
     */
    export function createDate(year: number, month: number, day: number): Date {
        return new Date(year, month - 1, day);
    }

    /**
     * 判断两个日期是否是同一天
     * @return 是同一天返回true，否则返回false
     */
    export function isSameDate(date1: Date, date2: Date): boolean {
        return date1.getDate() === date2.getDate() &&
            date1.getMonth() === date2.getMonth() &&
            date1.getFullYear() === date2.getFullYear();
    }

    /**
     * 返回下一周的这一天（即7天后）的Date的对象
     */
    export function toNextWeek(date: Date): Date {
        return new Date(date.getFullYear(), date.getMonth(), date.getDate() + 7);
    }

    /**
     * 返回上一周的这一天（即7天后）的Date的对象
     */
    export function toLastWeek(date: Date): Date {
        return new Date(date.getFullYear(), date.getMonth(), date.getDate() - 7);
    }
}