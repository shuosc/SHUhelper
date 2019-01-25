import {GetterTree} from "vuex";
import {State} from "./state";
import {RootState} from "~/store";
import {just} from "../../../../shared/tools/functools/maybe";

export const getters: GetterTree<State, RootState> = {
    student: (state: State) => {
        return just(state.student);
    }
};