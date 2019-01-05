import {CourseTime} from "../../../../shared/model/courseTime/courseTime";

export interface Course {
    readonly id: string,
    name: string,
    semesterId: string,
    teacherId: string,
    multipleTeacher: boolean,
    time: Array<CourseTime>,
    place: string
}

export interface State {
    courses: Array<Course> | null;
}

export const state = (): State => ({
    courses: null
});