import {GetterTree} from "vuex";
import {RootState} from "~/store";
import {State} from "~/store/modules/semester/state";
import {SemesterService} from "../../../../shared/model/semester/semester";
import {any} from "../../../../shared/tools/functools";

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
    },
    isHoliday: (state: State) => {
        return (date: Date) => {
            if (state.semesters === null) {
                return false;
            }
            return any(state.semesters.map(it => SemesterService.isHoliday(it, date)));
        }
    }
};