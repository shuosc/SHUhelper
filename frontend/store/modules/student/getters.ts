import {GetterTree} from "vuex";
import {State} from "./state";
import {RootState} from "~/store";

export const getters: GetterTree<State, RootState> = {
    isLogged: (state: State) => {
        return state.student !== null;
    },
    getName: (state: State) => {
        if (state.student === null || state.student === undefined) {
            return '游客'
        }
        return state.student.name;
    },
    getToken: (state: State) => {
        if (state.student !== null) {
            return state.student.token;
        }
        return null;
    }
};