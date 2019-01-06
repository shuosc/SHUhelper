import {Semester} from "../../../../shared/model/semester/semester";

export interface State {
    semesters: Array<Semester>;
}

export const state = (): State => ({
    semesters: []
});