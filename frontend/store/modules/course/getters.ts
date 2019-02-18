import {GetterTree} from "vuex";
import {RootState} from "~/store";
import {State} from "~/store/modules/course/state";
import {Course, CourseService} from "../../../../shared/model/course/course";
import {find} from "../../../../shared/tools/functools/array/array";
import {Semester} from "../../../../shared/model/semester/semester";
import {ClassService} from "../../../../shared/model/course/class/class";
import extractClasses = CourseService.extractClasses;
import isOnDate = ClassService.isOnDate;

export const getters: GetterTree<State, RootState> = {
    courses: (state: State) => {
        return state.courses;
    },
    getCourse: (state: State) => {
        return (id: any) => find(state.courses, (course: Course) => course.id === id);
    },
    classes: (state: State) => {
        return extractClasses(state.courses);
    },
    getClassesForDate: (state: State) => {
        return (semester: Semester, date: Date) => {
            return extractClasses(state.courses)
                .filter(class_ => isOnDate(class_, semester, date));
        }
    }
};