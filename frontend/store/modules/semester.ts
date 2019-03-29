import {ActionTree, GetterTree, MutationTree} from "vuex";
import {findFirst} from "fp-ts/lib/Array";
import {Option} from "fp-ts/lib/Option";
import {RootState} from "~/store";
import {Semester} from "../../../shared/model/semester/semester";
import {normalizeDateTimeInObject} from "~/tools/dateTime";
import {_, partial} from "~/tools/partial";
import {isWithinInterval} from "date-fns";

export const name = 'semester';
export const Types = {
    ADD_SEMESTER: 'addSemester'
};

export interface SemesterState {
    semesters: Array<Semester>;
}

export const state = (): SemesterState => ({
    semesters: []
});

export const getters: GetterTree<SemesterState, RootState> = {
    semesterForDate(state: SemesterState): (date: Date) => Option<Semester> {
        return (date: Date) => {
            const semesters: Array<Semester> = state.semesters.map(normalizeDateTimeInObject);
            return findFirst(semesters, partial(isWithinInterval, date));
        }
    }
};

export const mutations: MutationTree<SemesterState> = {
    [Types.ADD_SEMESTER]: (state: SemesterState, toAdd: Semester) => {
        if (findFirst(state.semesters, semester => semester._id === toAdd._id).isNone()) {
            state.semesters.push(toAdd);
        }
    }
};

export const actions: ActionTree<SemesterState, RootState> = {
    async fetchSemester({commit, state}, payload: { forDate: Date } | { id: any }) {
        const semesters = normalizeDateTimeInObject(state.semesters);
        if (payload.hasOwnProperty('forDate')) {
            if (findFirst(semesters, partial(isWithinInterval, (payload as any).forDate, _)).isNone()) {
                const data = await (this as any).$axios.$get(`/api/semester/?time=${(payload as any).forDate.toISOString()}`);
                if (data)
                    commit(Types.ADD_SEMESTER, data);
            }
        } else if (payload.hasOwnProperty('id')) {
            if (findFirst(semesters, partial(isWithinInterval, (payload as any).forDate, _)).isNone()) {
                const data = await (this as any).$axios.$get(`/api/semester/${(payload as any).id}`);
                if (data)
                    commit(Types.ADD_SEMESTER, data);
            }
        }
    },
    async fetchCurrent({commit}) {
        let data = await (this as any).$axios.$get(`/api/semester/?time=current`);
        commit(Types.ADD_SEMESTER, data);
    }
};

export const namespaced = true;
