import {State} from './state';
import {ActionContext, ActionTree} from 'vuex';
// import axios from 'axios';
import {RootState} from "~/store";
import {Types} from "~/store/modules/user/types";

export interface Actions<S, R> extends ActionTree<S, R> {
    doLogin: (context: ActionContext<S, R>, payload: any) => void;
    doLogout: (context: ActionContext<S, R>, payload: any) => void;
}

export const actions: Actions<State, RootState> = {
    doLogin: async function ({commit}, payload: { username: string, password: string }) {
        let data = await (this.$axios as any).$post('/auth/login', payload);
        commit(Types.SET_USER, {
            user: {
                name: data.name,
                token: data.token
            }
        });
    },
    doLogout: async function ({commit}) {
        commit(Types.SET_USER, {user: null});
    }
};