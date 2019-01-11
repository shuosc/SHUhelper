import {Course as SharedCourse} from "../../../../shared/model/course/course";

export interface Course extends SharedCourse {
    color: string;
}

export interface State {
    courses: Array<Course>;
}

export const state = (): State => ({
    courses: []
});