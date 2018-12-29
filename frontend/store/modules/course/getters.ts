import {GetterTree} from "vuex";
import {State} from "./state";
import {RootState} from "~/store";

export const getters: GetterTree<State, RootState> = {
    getCourses: (state: State) => {
        if (state.courses === null) {

        }
        return state.courses;
    }
};