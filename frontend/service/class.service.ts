import {Class} from "../../shared/model/course/class/class";
import {findFirst} from "fp-ts/lib/Array";
import {DateTimeInSemester, DateTimeInSemesterService} from "~/service/dateTimeInSemester.service";

export namespace ClassService {
    /**
     * 判断在某一天是否要上某节课
     */
    export function isOnDate(class_: Class, date: DateTimeInSemester): boolean {
        return DateTimeInSemesterService.isWorkingDay(date)
            && date.dateTime.getDay() === class_.day
            && findFirst(class_.weeks, week => DateTimeInSemesterService.getWorkWeekIndex(date) === week).isSome();
    }

    /**
     * 能判断第几节课是否在上某节课
     */
    export function isOnSector(class_: Class, sectorIndex: number): boolean {
        return class_.beginSector - 1 <= sectorIndex
            && sectorIndex <= class_.endSector - 1;
    }

    /**
     * 能判断某个时间是否在上某节课
     */
    export function isOnDateTime(class_: Class, date: DateTimeInSemester): boolean {
        return isOnDate(class_, date) && isOnSector(class_, DateTimeInSemesterService.currentSectorIndex(date).getOrElse(0));
    }
}