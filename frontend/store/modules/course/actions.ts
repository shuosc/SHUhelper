import {ActionContext, ActionTree} from "vuex";
import {RootState} from "~/store";
import {State} from "~/store/modules/course/state";
import {Types} from "~/store/modules/course/types";
import {Course} from "../../../../shared/model/course/course";

export interface Actions<S, R> extends ActionTree<S, R> {
    fetchCourses: (context: ActionContext<S, R>, payload: any) => void;
}

export const actions: Actions<State, RootState> = {
    fetchCourses: async function ({commit, state, rootState, dispatch}) {
        if (rootState.student.student !== null) {
            let data: Array<Course> = await Promise.all(rootState.student.student.courseIds.map((id) => (this.$axios as any).$get('/api/course/' + id)));
            commit(Types.SET_COURSES, {
                data
            });
            await Promise.all(data.map(it => dispatch('semester/fetchSemesterIfNecessary', {id: it.semesterId}, {root: true})));
        }
    }
};