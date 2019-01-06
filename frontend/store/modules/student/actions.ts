import {State} from './state';
import {ActionContext, ActionTree} from 'vuex';
import {RootState} from "~/store";
import {Types} from "~/store/modules/student/types";

export interface Actions<S, R> extends ActionTree<S, R> {
    doLogin: (context: ActionContext<S, R>, payload: any) => void;
    doLogout: (context: ActionContext<S, R>, payload: any) => void;
}

export const actions: Actions<State, RootState> = {
    doLogin: async function ({commit}, payload: { username: string, password: string }) {
        let data = await (this.$axios as any).$post('/auth/login', payload);
        (this.$axios as any).setToken(data.token, 'Bearer');
        let studentInfo = await (this.$axios as any).$get('/api/student');
        commit(Types.SET_STUDENT, {
            student: {
                ...data,
                ...studentInfo
            }
        });
    },
    doLogout: async function ({commit}) {
        commit(Types.SET_STUDENT, {student: null});
    }
};