import {ActionContext, ActionTree} from "vuex";
import {RootState} from "~/store";
import {State} from "~/store/modules/course/state";
import {Types} from "~/store/modules/course/types";

export interface Actions<S, R> extends ActionTree<S, R> {
    fetchCourses: (context: ActionContext<S, R>, payload: any) => void;
}

export const actions: Actions<State, RootState> = {
    fetchCourses: async function ({commit}) {
        let data = await (this.$axios as any).$get('/api/courses');
        commit(Types.SET_COURSES, {
            data
        });
    }
};