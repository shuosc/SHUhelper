import {DAY_CHINESE_TO_NUMBER} from "../tools/date";

export class CourseTime {
    constructor(public day: number,
                public beginSector: number,
                public endSector: number) {
    }

    static fromRawObject(rawObject: any): CourseTime {
        return new CourseTime(rawObject['day'], rawObject['beginSector'], rawObject['endSector']);
    }

    static fromString(str: string): CourseTime | null {
        const regex = /([一二三四五六日])(\d+)-(\d+)/;
        let result = regex.exec(str);
        if (result === null)
            return null;
        return new CourseTime(DAY_CHINESE_TO_NUMBER.get(str[0]) as number, parseInt(result[2]), parseInt(result[3]));
    }

    serialize() {
        return this;
    }
}