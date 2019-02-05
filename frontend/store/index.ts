import Vue from 'vue';
import Vuex from 'vuex';
import * as student from './modules/student';
import * as courses from './modules/course';
import * as semesters from './modules/semester';
import * as admin from './modules/admin';
import * as root from './root';

Vue.use(Vuex);

interface ModulesStates {
    student: student.State;
    courses: courses.State;
    semester: semesters.State;
    admin: admin.State;
}

export type RootState = root.State & ModulesStates;
export default () => new Vuex.Store({
    state: root.state() as any,
    getters: root.getters,
    mutations: root.mutations,
    actions: root.actions as any,
    modules: {
        [student.name]: student,
        [courses.name]: courses,
        [semesters.name]: semesters,
        [admin.name]: admin,
    }
});