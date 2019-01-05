import {DAY_CHINESE_TO_NUMBER} from "../../tools/date";

export interface CourseTime {
    readonly day: number;
    readonly beginSector: number;
    readonly endSector: number;
}

export namespace CourseTimeService {
    export function fromString(str: string): CourseTime | null {
        const regex = /([一二三四五六日])(\d+)-(\d+)/;
        let result = regex.exec(str);
        if (result === null)
            return null;
        return {
            day: DAY_CHINESE_TO_NUMBER.get(str[0]),
            beginSector: parseInt(result[2]),
            endSector: parseInt(result[3])
        }
    }
}

