import {MutationTree} from "vuex";
import {State} from "./state";
import {Types} from "./types";

export const mutations: MutationTree<State> = {
    [Types.SET_STUDENT]: (state: State, payload: State) => {
        state.student = payload.student;
    }
};