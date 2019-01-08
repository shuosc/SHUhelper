import {GetterTree} from "vuex";
import {RootState} from "~/store";
import {State} from "~/store/modules/course/state";
import {DateRangeService} from "../../../../shared/model/dateRange/dateRange";
import {Course, CourseService} from "../../../../shared/model/course/course";

export const getters: GetterTree<State, RootState> = {
    getCourses: (state: State) => {
        if (state.courses === null) {
            return null;
        }
        return state.courses;
    },
    getCoursesForDate: (state: State, _: any, rootState: RootState) => {
        const hasClassOnDate = (course: Course, date: Date) => {
            const semester = rootState.semester.semesters.find(it => DateRangeService.isDateIn(it, date));
            if (semester === undefined)
                return false;
            return CourseService.hasClassOnDate(course, semester, date);
        };
        return (date: Date) => {
            return state.courses.filter((it) => hasClassOnDate(it, date));
        }
    }
};