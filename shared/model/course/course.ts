import {Class, ClassService} from "./class/class";
import {Semester} from "../semester/semester";
import {assert} from "../../tools/assert";
import {DateRangeService} from "../dateRange/dateRange";

/**
 * 课程模型
 */
export interface Course {
    readonly id: string;
    readonly name: string;
    readonly teacherId: any;
    readonly semesterId: any;
    readonly classes: Array<Class>;
    readonly place: string;
}

export namespace CourseService {
    /**
     * 判断某节课是否是某个学期内的课
     */
    export function isInSemester(course: Course, semester: Semester): boolean {
        return course.semesterId === semester._id;
    }

    /**
     * 判断某个课程是否在某天有课
     */
    export function hasClassOnDate(course: Course, semester: Semester, date: Date) {
        assert(DateRangeService.isDateIn(semester, date));
        for (let class_ of course.classes) {
            if (ClassService.isOnDate(class_, semester, date)) {
                return true;
            }
        }
        return false;
    }
}
