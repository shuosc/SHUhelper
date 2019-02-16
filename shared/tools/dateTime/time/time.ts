import {just, Maybe} from "../../functools/maybe";

export namespace TimeService {
    /**
     * 创建一个时间对象
     */
    export function createTime(hour: number, minute: number, second: number = 0): Date {
        return new Date(0, 0, 0, hour, minute, second);
    }

    export function createTimeFromString(str: string): Maybe<Date> {
        const toNumber = str.split(':').map(it => parseInt(it));
        if ((toNumber.length !== 2 && toNumber.length !== 3) || toNumber.some(it => isNaN(it))) {
            return new Maybe<Date>(null);
        }
        if (toNumber.length === 2) {
            return just(createTime(toNumber[0], toNumber[1]));
        } else {
            return just(createTime(toNumber[0], toNumber[1], toNumber[2]));
        }
    }

    /**
     * 从日期时间对象中提取纯时间对象
     */
    function extractTime(dateTime: Date): Date {
        return createTime(dateTime.getHours(), dateTime.getMinutes(), dateTime.getSeconds());
    }

    /**
     * 返回两个时间点之间的时间差，注意只比较时间部分，忽略日期部分
     * @return 单位为毫秒的时间差
     */
    export function timeDistance(now: Date, target: Date): number {
        const nowTime = extractTime(now);
        const targetTime = extractTime(target);
        return Math.abs(nowTime.getTime() - targetTime.getTime());
    }

    /**
     * 判断 @arg now 的 时间 是否早于 @arg target，只比较时间部分，忽略日期部分
     * @note 不包含等于的情况
     */
    export function earlierThan(now: Date, target: Date): boolean {
        const nowTime = extractTime(now);
        const targetTime = extractTime(target);
        return nowTime.getTime() < targetTime.getTime();
    }

    /**
     * 判断 @arg now 的 时间 是否晚于 @arg target，只比较时间部分，忽略日期部分
     * @note 包含等于的情况
     */
    export function laterThan(now: Date, target: Date): boolean {
        const nowTime = extractTime(now);
        const targetTime = extractTime(target);
        return nowTime.getTime() >= targetTime.getTime();
    }

    export function timestampDifferenceToSeconds(timestampDifference: number): number {
        return Math.round(timestampDifference / 1000);
    }

    export function timestampDifferenceToMinutes(timestampDifference: number): number {
        return Math.round(timestampDifference / 1000 / 60);
    }

    export function timestampDifferenceToDay(timestampDifference: number): number {
        return Math.round(timestampDifference / 1000 / 60 / 60 / 24);
    }
}