import {clone} from "../../../tools/clone";
import {Maybe} from "../../../tools/functools/maybe";
import {findIndex} from "../../../tools/functools/find";
import {TimeService} from "../../../tools/time/time";

function createTime(hour: number, minute: number): Date {
    return new Date(0, 0, 0, hour, minute);
}

export const SECTOR_TO_START_TIME = [
    createTime(8, 0),
    createTime(8, 55),
    createTime(10, 0),
    createTime(10, 55),
    createTime(12, 10),
    createTime(13, 5),
    createTime(14, 10),
    createTime(15, 5),
    createTime(16, 0),
    createTime(16, 55),
    createTime(18, 0),
    createTime(18, 55),
    createTime(19, 40),
];

export namespace SectorService {
    export function getSectorStartTime(sectorId: number): Date {
        return SECTOR_TO_START_TIME[sectorId - 1];
    }

    export function getSectorEndTime(sectorId: number): Date {
        let result = clone(getSectorStartTime(sectorId));
        result.setMinutes(result.getMinutes() + 45);
        return result;
    }

    export function isTimeInSector(time: Date, sectorId: number): boolean {
        const theTime = createTime(time.getHours(), time.getMinutes());
        return getSectorStartTime(sectorId) <= theTime && theTime < getSectorEndTime(sectorId);
    }

    /**
     * 判断某个时间是否在 @arg sectorId 之后的课间休息之中
     */
    export function isTimeBetweenSectors(time: Date, sectorId: number): boolean {
        return getSectorEndTime(sectorId) <= time && time < getSectorStartTime(sectorId + 1);
    }

    export function currentSector(time: Date): Maybe<number> {
        for (let sectorId = 1; sectorId <= SECTOR_TO_START_TIME.length; ++sectorId) {
            if (isTimeInSector(time, sectorId)) {
                return new Maybe(sectorId);
            }
        }
        return new Maybe<number>(null);
    }

    export function nextSector(time: Date): Maybe<number> {
        const nowTime = createTime(time.getHours(), time.getMinutes());
        return findIndex(SECTOR_TO_START_TIME, it => it > nowTime).map(it => it + 1);
    }

    export function minutesBetweenSectors(firstSectorId: number): number {
        const timestampDifference = TimeService.timeDistance(getSectorEndTime(firstSectorId), getSectorStartTime(firstSectorId + 1));
        return TimeService.timestampDifferenceToMinutes(timestampDifference);
    }

    export function isBeforeFirstSector(time: Date) {
        return TimeService.earlierThan(time, getSectorStartTime(1));
    }

    export function isAfterLastSector(time: Date) {
        return TimeService.earlierThan(getSectorEndTime(SECTOR_TO_START_TIME.length), time);
    }
}
