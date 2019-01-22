import {dayChineseToNumber} from "../../../tools/date/date";
import {Semester, SemesterService} from "../../semester/semester";
import {assert} from "../../../tools/assert";
import {DateRangeService} from "../../dateRange/dateRange";
import {Maybe} from "../../../tools/functools/maybe";

/**
 * 表示一节课
 */
export interface Class {
    readonly day: number;           // 周几的课
    readonly courseId: any;         // 所属课程
    readonly beginSector: number;   // 在第几节开始
    readonly endSector: number;     // 在第几节结束
    readonly weeks: Array<number>;  // 哪几周有这个课
}

export namespace ClassService {
    function parseWeeks(str: string): Array<number> {
        // 单双周课
        if (str.includes('单')) {
            return [1, 3, 5, 7, 9];
        } else if (str.includes('双')) {
            return [2, 4, 6, 8, 10];
        }
        // 某几周课
        // eg. 1,2 周
        str = str.replace('，', ',');
        const discreteWeeksRegex = /(\d+\s*(,\s*\d+\s*)+)周/g;
        let regexResult = discreteWeeksRegex.exec(str);
        if (regexResult !== null) {
            return regexResult[1]
                .split(',')
                .map(it => parseInt(it));
        }
        // 连续的几周课
        // eg. 4-10周
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

    /**
     * 从字符串中构造出一节课的信息
     */
    export function fromString(str: string, courseId: any): Maybe<Class> {
        const regex = /([一二三四五六日])(\d+)-(\d+)([^一二三四五]*)/;
        let result = new Maybe(regex.exec(str));
        return result.flatMap((infoColumns =>
            dayChineseToNumber(infoColumns[1]).map(day => {
                return {
                    day: day,
                    courseId: courseId,
                    beginSector: parseInt(infoColumns[2]),
                    endSector: parseInt(infoColumns[3]),
                    weeks: parseWeeks(infoColumns[4].trim())
                }
            }))
        );
    }

    /**
     * 判断在某一天是否要上某节课
     */
    export function isOnDate(class_: Class, semester: Semester, date: Date): boolean {
        assert(DateRangeService.isDateIn(semester, date), `${date} is not in ${semester.name}!`);
        const day = SemesterService.getSchoolDay(semester, date);
        if (day === SemesterService.HOLIDAY || day === 0 || day === 6) {
            return false;
        }
        const week = SemesterService.getWeekIndex(semester, date);
        return class_.day === day && class_.weeks.indexOf(week) !== -1;
    }

    export function isOnSector(class_: Class, sectorId: number): boolean {
        return class_.beginSector <= sectorId && sectorId <= class_.endSector;
    }
}
