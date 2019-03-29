import {ActionTree, GetterTree, MutationTree} from "vuex";

import {Course as SharedCourse} from "../../../shared/model/course/course";
import {RootState} from "~/store";
import {ClassService} from "~/service/class.service";
import {findFirst, flatten} from "fp-ts/lib/Array";
import {nextBeautifulLightColor} from "~/tools/color";
import {DateTimeInSemester} from "~/service/dateTimeInSemester.service";
import {_, partial} from "~/tools/partial";

export const name = 'course';

export const Types = {
    SET_COURSES: 'setCourses',
    ADD_COURSE: 'addCourse'
};

export interface Course extends SharedCourse {
    color: string;
}

export interface CourseState {
    courses: Array<Course>;
}

export const state = (): CourseState => ({
    courses: []
});

export const getters: GetterTree<CourseState, RootState> = {
    courses: (state: CourseState) => {
        return state.courses;
    },
    classesForDate: (state: CourseState) => {
        return (dateInSemester: DateTimeInSemester) => {
            const isOnDate = partial(ClassService.isOnDate, _, dateInSemester);
            return flatten(state.courses.map(it => it.classes))
                .filter(isOnDate);
        }
    },
    course(state: CourseState) {
        return (id: any) => {
            return findFirst(state.courses, it => it.id === id);
        }
    }
};

export const mutations: MutationTree<CourseState> = {
    [Types.SET_COURSES]: (state: CourseState, payload: { courses: Array<SharedCourse> }) => {
        state.courses = payload.courses.map((it: SharedCourse): Course => {
            return {
                ...it,
                color: nextBeautifulLightColor()
            }
        });
    },
    [Types.ADD_COURSE]: (state: CourseState, payload: { course: SharedCourse }) => {
        if (findFirst(state.courses, course => course.id === payload.course.id).isSome()) {
            return;
        }
        state.courses.push({
            ...payload.course,
            color: nextBeautifulLightColor()
        });
    }
};

export const actions: ActionTree<CourseState, RootState> = {
    fetchCourses: async function ({commit, state, dispatch, rootState}) {
        const student = (rootState as any).student.student;
        if (student !== null) {
            const fetchCourse = (id: string) => (this as any).$axios.$get('/api/course/' + id);
            const unfetched = student.courseIds.filter(courseId => findFirst(state.courses, course => course.id === courseId).isNone());
            const data: Array<SharedCourse> = await Promise.all(unfetched.map(fetchCourse)) as any as Array<SharedCourse>;
            data.map(it => commit(Types.ADD_COURSE, {course: it}));
        }
    }
};

export const namespaced = true;
