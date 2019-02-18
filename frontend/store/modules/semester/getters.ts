import {GetterTree} from "vuex";
import {RootState} from "~/store";
import {State} from "~/store/modules/semester/state";
import {Maybe} from "../../../../shared/tools/functools/maybe";
import {DateRangeService} from "../../../../shared/model/dateRange/dateRange";
import * as _ from "lodash";
import {find} from "../../../../shared/tools/functools/array/array";

export const getters: GetterTree<State, RootState> = {
    getSemester: (state: State) => {
        return (id: string) => {
            return find(state.semesters, it => it._id === id);
        }
    },
    getSemesterForDate: (state: State) => {
        return (date: Date) => {
            const semesters = new Maybe(state.semesters);
            const isDateIn = _.partial(DateRangeService.isDateIn, _, date);
            return semesters.flatMap(semesters => find(semesters, isDateIn));
        }
    },
    semesters: (state: State) => {
        return state.semesters;
    }
};