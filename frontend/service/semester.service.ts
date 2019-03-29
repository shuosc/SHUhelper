import {Semester} from "../../shared/model/semester/semester";
import {DateTimeInSemesterService} from "./dateTimeInSemester.service";
import {eachDayOfInterval, isWithinInterval} from "date-fns";

export namespace SemesterService {
    /**
     * 获取总的工作日数量
     */
    export function getTotalWorkingDayCount(semester: Semester) {
        return getWorkingDayCount(semester, semester.start, semester.end);
    }

    /**
     * 获取从@arg from 开始到 @arg to 的工作日数量
     */
    export function getWorkingDayCount(semester: Semester, from: Date, to: Date): number {
        const targetRange = {start: from, end: to};
        return eachDayOfInterval(semester)
            .filter(it => isWithinInterval(it, targetRange))
            .map(it => {
                return {semester: semester, dateTime: it}
            })
            .filter(DateTimeInSemesterService.isWorkingDay)
            .length;
    }
}
