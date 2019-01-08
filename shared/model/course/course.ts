import {CourseTime} from "./courseTime/courseTime";
import {Semester} from "../semester/semester";

export interface Course {
    readonly id: any;
    readonly name: string;
    readonly teacherId: any;
    readonly semesterId: any;
    readonly times: Array<CourseTime>;
    readonly place: string;
}

export namespace CourseService {
    export function isInSemester(course: Course, semester: Semester): boolean {
        return course.semesterId === semester._id;
    }

    export function hasClassOnDay(course: Course, day: number): boolean {
        for (const time of course.times) {
            if (time.day === day) {
                return true;
            }
        }
        return false;
    }
}
