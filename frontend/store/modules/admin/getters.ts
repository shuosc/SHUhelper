import {GetterTree} from "vuex";
import {RootState} from "~/store";
import {State} from "~/store/modules/admin/state";

export const getters: GetterTree<State, RootState> = {
    token: (state: State) => {
        return state.token;
    },
};