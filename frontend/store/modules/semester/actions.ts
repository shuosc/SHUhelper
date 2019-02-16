import {ActionContext, ActionTree} from "vuex";
import {RootState} from "~/store";
import {State} from "./state";
import {Types} from "./types";
import {DateTimeService} from "../../../../shared/tools/dateTime/dateTime";
import {Semester} from "../../../../shared/model/semester/semester";

export interface Actions<S, R> extends ActionTree<S, R> {
    fetchCurrentSemester: (context: ActionContext<S, R>) => void;
    fetchSemesterIfNecessary: (context: ActionContext<S, R>, payload: { id: string }) => void;
    fetchAllSemester: (context: ActionContext<S, R>) => void;
    postSemester: (context: ActionContext<S, R>, payload: { semester: Semester }) => void;
    putSemester: (context: ActionContext<S, R>, payload: { semester: Semester }) => void;
    deleteSemester: (context: ActionContext<S, R>, payload: { semester: Semester }) => void;
}

export const actions: Actions<State, RootState> = {
    fetchCurrentSemester: async function ({commit}) {
        let data = await (this.$axios as any).$get('/api/semester/current');
        commit(Types.ADD_SEMESTER, {
            data: DateTimeService.normalizeDateTimeInObject(data)
        });
    },
    fetchSemesterIfNecessary: async function ({commit, state}, payload: { id: string }) {
        if (state.semesters.find(it => it._id === payload.id) === undefined) {
            let data = await (this.$axios as any).$get('/api/semester/' + payload.id);
            commit(Types.ADD_SEMESTER, {
                data: DateTimeService.normalizeDateTimeInObject(data)
            });
        }
    },
    fetchAllSemester: async function ({commit}) {
        let data = await (this.$axios as any).$get('/api/semesters');
        data.map((semester: any) => {
            commit(Types.ADD_SEMESTER, {
                data: DateTimeService.normalizeDateTimeInObject(semester)
            });
        });
    },
    postSemester: async function ({commit, state, rootState}) {
        let result = await (this.$axios as any).$post(`/api/semester/`, {
            begin: new Date(),
            end: new Date(),
            holidays: [],
            name: "新的学期"
        }, {
            headers: {
                adminToken: rootState.admin.token
            }
        });
        commit(Types.ADD_SEMESTER, {
            data: DateTimeService.normalizeDateTimeInObject(result.result)
        });
    },
    putSemester: async function ({commit, state, rootState}, payload: { semester: Semester }) {
        await (this.$axios as any).$put(`/api/semester/${payload.semester._id}`, payload.semester, {
            headers: {
                adminToken: rootState.admin.token
            }
        });
        commit(Types.SET_SEMESTER, payload);
    },
    deleteSemester: async function ({commit, state, rootState}, payload: { semester: Semester }) {
        await (this.$axios as any).$delete(`/api/semester/${payload.semester._id}`, {
            headers: {
                adminToken: rootState.admin.token
            }
        });
        commit(Types.REMOVE_SEMESTER, payload);
    }
};
