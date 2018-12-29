import {CourseTime} from "../../../../shared/model/courseTime";

interface Course {
    readonly id: string,
    name: string,
    semesterId: string,
    teacherId: string,
    multipleTeacher: boolean,
    time: CourseTime,
    place: string
}


export interface State {
    courses: Array<Course> | null;
}

export const state = (): State => ({
    courses: null
});