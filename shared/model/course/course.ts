import {Class, ClassService} from "./class/class";
import {Semester} from "../semester/semester";
import {assert} from "../../tools/assert";
import {DateRangeService} from "../dateRange/dateRange";

export interface Course {
    readonly id: string;
    readonly name: string;
    readonly teacherId: any;
    readonly semesterId: any;
    readonly classes: Array<Class>;
    readonly place: string;
}

export namespace CourseService {
    export function isInSemester(course: Course, semester: Semester): boolean {
        return course.semesterId === semester._id;
    }

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
