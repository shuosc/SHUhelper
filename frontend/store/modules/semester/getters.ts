import {GetterTree} from "vuex";
import {RootState} from "~/store";
import {State} from "~/store/modules/semester/state";

export const getters: GetterTree<State, RootState> = {
    getSemester: (state: State) => {
        return (id: string) => {
            if (state.semesters === null) {
                return null;
            }
            return state.semesters.find(it => it._id === id);
        }
    },
    getSemesterForDate: (state: State) => {
        return (date: Date) => {
            if (state.semesters === null) {
                return null;
            }
            return state.semesters.find(it => {
                return it.begin <= date && date < it.end;
            });
        }
    }
};