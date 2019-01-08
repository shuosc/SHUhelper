import {DAY_CHINESE_TO_NUMBER} from "../../../tools/date";

export interface CourseTime {
    readonly day: number;
    readonly beginSector: number;
    readonly endSector: number;
    readonly weeks: Array<number>;
}

export namespace CourseTimeService {
    function parseWeeks(str: string): Array<number> {
        if (str.includes('单')) {
            return [1, 3, 5, 7, 9];
        } else if (str.includes('双')) {
            return [2, 4, 6, 8, 10];
        }
        str = str.replace('，', ',');
        const discreteWeeksRegex = /(\d+\s*(,\s*\d+\s*)+)周/g;
        let regexResult = discreteWeeksRegex.exec(str);
        if (regexResult !== null) {
            return regexResult[1]
                .split(',')
                .map(it => parseInt(it));
        }
        const continuousWeeksRegex = /(\d+)\s*-\s*(\d+)\s*周/g;
        regexResult = continuousWeeksRegex.exec(str);
        if (regexResult !== null) {
            let result = [];
            for (let i = parseInt(regexResult[1]); i <= parseInt(regexResult[2]); ++i) {
                result.push(i);
            }
            return result;
        }
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    }

    export function fromString(str: string): CourseTime | null {
        const regex = /([一二三四五六日])(\d+)-(\d+)([^一二三四五]*)/;
        let result = regex.exec(str);
        if (result === null)
            return null;
        const day = DAY_CHINESE_TO_NUMBER.get(str[0]);
        if (day === undefined) {
            return null;
        }
        return {
            day: day,
            beginSector: parseInt(result[2]),
            endSector: parseInt(result[3]),
            weeks: parseWeeks(result[4].trim())
        }
    }
}

