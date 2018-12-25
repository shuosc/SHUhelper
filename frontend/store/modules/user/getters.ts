import {GetterTree} from "~/node_modules/vuex";
import {State} from "./state";
import {RootState} from "~/store";

export const getters: GetterTree<State, RootState> = {
    isLogged: (state: State) => {
        return state.user !== null;
    },
    getName: (state: State) => {
        if (state.user === null || state.user === undefined) {
            return '游客'
        }
        return state.user.name;
    }
};