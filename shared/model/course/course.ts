import {Class, ClassService} from "./class/class";
import {Semester} from "../semester/semester";
import {assert} from "../../tools/assert";
import {DateRangeService} from "../dateRange/dateRange";
import * as _ from "lodash";

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
        const isOnDate = _.partial(ClassService.isOnDate, _, semester, date);
        return course.classes.some(isOnDate);
    }

    /**
     * 从课程列表中解出所有的课
     */
    export function extractClasses(courses: Array<Course>): Array<Class> {
        return courses.map(it => it.classes)
            .reduce((classes1, classes2) => classes1.concat(classes2), [])
    }
}
