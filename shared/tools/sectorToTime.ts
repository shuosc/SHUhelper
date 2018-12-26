import {clone} from "./clone";

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

export function toEndTime(time: Date) {
    let result = clone(time);
    result.setMinutes(time.getMinutes() + 45);
    return result;
}