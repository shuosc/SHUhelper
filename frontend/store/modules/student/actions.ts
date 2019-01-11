import {State} from './state';
import {ActionContext, ActionTree, Commit} from 'vuex';
import {RootState} from "~/store";
import {Types} from "~/store/modules/student/types";

export interface Actions<S, R> extends ActionTree<S, R> {
    doLogin: (context: ActionContext<S, R>, payload: { username: string, password: string }) => void;
    doLogout: (context: ActionContext<S, R>, payload: any) => void;
    restoreLogin: (context: ActionContext<S, R>, payload: { token: string }) => void;
}

async function getStudentInfo(commit: Commit, axios: any, token: string) {
    axios.setToken(token, 'Bearer');
    let studentInfo = await axios.$get('/api/student');
    commit(Types.SET_STUDENT, {
        student: {
            token: token,
            ...studentInfo
        }
    });
}

export const actions: Actions<State, RootState> = {
    doLogin: async function ({commit}, payload: { username: string, password: string }) {
        let data = await (this.$axios as any).$post('/auth/login', payload);
        console.log(data);
        await getStudentInfo(commit, this.$axios as any, data.token);
    },
    doLogout: async function ({commit}) {
        commit(Types.SET_STUDENT, {student: null});
    },
    restoreLogin: async function ({commit}, payload: { token: string }) {
        await getStudentInfo(commit, this.$axios as any, payload.token);
    },
};