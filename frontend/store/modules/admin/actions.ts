import {ActionContext, ActionTree} from "vuex";
import {RootState} from "~/store";
import {State} from "./state";
import {Types} from "~/store/modules/admin/types";

export interface Actions<S, R> extends ActionTree<S, R> {
    checkToken: (context: ActionContext<S, R>, payload: { token: string }) => Promise<boolean>;
}

export const actions: Actions<State, RootState> = {
    checkToken: async function ({commit, state, rootState, dispatch}, payload: { token: string }) {
        let result = await (this.$axios as any).$post('/auth/check-token', payload);
        if (!result.success)
            commit(Types.SET_TOKEN, "");
        else
            commit(Types.SET_TOKEN, payload);
        return result.success;
    }
};