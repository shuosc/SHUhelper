import {MutationTree} from "vuex";
import {State} from "./state";
import {Types} from "./types";
import {Semester} from "../../../../shared/model/semester/semester";

export const mutations: MutationTree<State> = {
    [Types.SET_SEMESTERS]: (state: State, payload: any) => {
        state.semesters = payload.data;
    },
    [Types.ADD_SEMESTER]: (state: State, payload: any) => {
        if (state.semesters === null) {
            state.semesters = [payload.data];
        } else {
            if (state.semesters.find(it => it._id === payload.data._id) === undefined) {
                state.semesters.push(payload.data);
            }
        }
    },
    [Types.SET_SEMESTER]: (state: State, payload: { semester: Semester }) => {
        state.semesters.map(it => {
            if (payload.semester._id === it._id) {
                return payload.semester;
            }
            return it;
        })
    },
    [Types.REMOVE_SEMESTER]: (state: State, payload: { semester: Semester }) => {
        state.semesters.splice(state.semesters.findIndex(it => it._id === payload.semester._id))
    }
};