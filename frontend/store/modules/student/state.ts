import {Student as SharedStudent} from "../../../../shared/model/student/student";

export interface Student extends SharedStudent {
    readonly token: string;
}

export interface State {
    student: Student | null;
}

export const state = (): State => ({
    student: null
});