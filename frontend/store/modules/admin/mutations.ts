import {MutationTree} from "vuex";
import {State} from "./state";
import {Types} from "./types";

export const mutations: MutationTree<State> = {
    [Types.SET_TOKEN]: (state: State, payload: any) => {
        state.token = payload.token;
    }
};