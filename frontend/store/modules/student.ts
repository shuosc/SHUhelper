import {ActionTree, GetterTree, MutationTree} from "vuex";
import {RootState} from "store";
import {fromNullable, Option} from "fp-ts/lib/Option";
import {Student} from "../../../shared/model/student/student";

export const name = "student";

export const Types = {
    SET: 'SET'
};

export interface StudentState {
    student: Student | null,
    token: string
}

export const state = (): StudentState => ({
    student: null,
    token: ''
});

export const getters: GetterTree<StudentState, RootState> = {
    student(state: StudentState): Option<Student> {
        return fromNullable(state.student);
    },
    token(state: StudentState): string {
        return state.token;
    }
};

export const mutations: MutationTree<StudentState> = {
    [Types.SET]: (state: StudentState, newState: StudentState) => {
        state.token = newState.token;
        state.student = newState.student;
    }
};

async function getStudentInfo(commit: any, axios: any, token: string) {
    axios.setToken(token, 'Bearer');
    let studentInfo = await axios.$get('/api/student');
    commit(Types.SET, {
        token: token,
        student: studentInfo
    });
}

export const actions: ActionTree<StudentState, RootState> = {
    async login({commit}, payload: { username: string, password: string }) {
        let data = await (this as any).$axios.$post('/auth/login', payload);
        await getStudentInfo(commit, (this as any).$axios, data.token);
    },

    async logout({commit}) {
        commit(Types.SET, {student: null, token: ''});
    },

    async restoreLogin({commit}, payload: { token: string }) {
        await getStudentInfo(commit, (this as any).$axios, payload.token);
    }
};

export const namespaced = true;