import {MutationTree} from "vuex";
import {State} from "./state";
import {Types} from "./types";

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
    }
};