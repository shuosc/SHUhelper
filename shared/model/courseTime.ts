import {DAY_CHINESE_TO_NUMBER} from "../tools/date";

export class CourseTime {
    constructor(public day: number,
                public beginSector: number,
                public endSector: number) {
    }

    static fromRawObject(rawObject): CourseTime {
        return new CourseTime(rawObject['day'], rawObject['beginSector'], rawObject['endSector']);
    }

    static fromString(str: string) {
        const regex = /([一二三四五六日])(\d+)-(\d+)/;
        let result = regex.exec(str);
        return new CourseTime(DAY_CHINESE_TO_NUMBER.get(str[0]), parseInt(result[2]), parseInt(result[3]));
    }

    serialize() {
        return this;
    }
}