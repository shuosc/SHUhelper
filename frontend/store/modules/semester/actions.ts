import {ActionContext, ActionTree} from "vuex";
import {RootState} from "~/store";
import {State} from "./state";
import {Types} from "./types";
import {SemesterJson, SemesterService} from "../../../../shared/model/semester/semester";

export interface Actions<S, R> extends ActionTree<S, R> {
    fetchSemesterIfNecessary: (context: ActionContext<S, R>, payload: any) => void;
}

export const actions: Actions<State, RootState> = {
    fetchSemesterIfNecessary: async function ({commit, state}, payload: { id: string }) {
        if (state.semesters === null || state.semesters.find(it => it._id === payload.id) === undefined) {
            let data: SemesterJson = await (this.$axios as any).$get('/api/semester/' + payload.id);
            commit(Types.ADD_SEMESTER, {
                data: SemesterService.normalize(data)
            });
        }
    }
};