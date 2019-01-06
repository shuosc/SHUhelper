import {Course} from "../../../../shared/model/course/course";

export interface State {
    courses: Array<Course>;
}

export const state = (): State => ({
    courses: []
});