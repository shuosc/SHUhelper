import {ActionContext, ActionTree} from "vuex";
import {RootState} from "~/store";
import {State} from "./state";
import {Types} from "./types";
import * as dateNormalizer from "date-normalizer";

const normalizeDateInObject = (dateNormalizer as any)['date-normalizer'].normalizeDateInObject;

export interface Actions<S, R> extends ActionTree<S, R> {
    fetchCurrentSemester: (context: ActionContext<S, R>) => void;
    fetchSemesterIfNecessary: (context: ActionContext<S, R>, payload: any) => void;
}

export const actions: Actions<State, RootState> = {
    fetchCurrentSemester: async function ({commit, state}) {
        let data = await (this.$axios as any).$get('/api/semester/current');
        commit(Types.ADD_SEMESTER, {
            data: normalizeDateInObject(data)
        });
    },
    fetchSemesterIfNecessary: async function ({commit, state}, payload: { id: string }) {
        if (state.semesters.find(it => it._id === payload.id) === undefined) {
            let data = await (this.$axios as any).$get('/api/semester/' + payload.id);
            commit(Types.ADD_SEMESTER, {
                data: normalizeDateInObject(data)
            });
        }
    }
};