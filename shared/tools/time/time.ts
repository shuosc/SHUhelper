export namespace TimeService {
    /**
     * 创建一个时间对象
     */
    export function createTime(hour: number, minute: number, second: number = 0): Date {
        return new Date(0, 0, 0, hour, minute, second);
    }

    /**
     * 返回两个时间点之间的时间差
     * @return 单位为毫秒的时间差
     */
    export function timeDistance(now: Date, target: Date): number {
        const nowTime = createTime(now.getHours(), now.getMinutes(), now.getSeconds());
        const targetTime = createTime(target.getHours(), target.getMinutes(), target.getSeconds());
        return Math.abs(nowTime.getTime() - targetTime.getTime());
    }

    /**
     * 判断 @arg now 的 时间 是否早于 @arg target
     */
    export function earlierThan(now: Date, target: Date): boolean {
        const nowTime = createTime(now.getHours(), now.getMinutes(), now.getSeconds());
        const targetTime = createTime(target.getHours(), target.getMinutes(), target.getSeconds());
        return nowTime.getTime() < targetTime.getTime();
    }

    /**
     * 判断 @arg now 的 时间 是否晚于 @arg target
     */
    export function laterThan(now: Date, target: Date): boolean {
        const nowTime = createTime(now.getHours(), now.getMinutes(), now.getSeconds());
        const targetTime = createTime(target.getHours(), target.getMinutes(), target.getSeconds());
        return nowTime.getTime() > targetTime.getTime();
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