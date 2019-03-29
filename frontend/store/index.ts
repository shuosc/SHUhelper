import * as student from './modules/student'
import * as semester from './modules/semester'
import * as course from './modules/course'

export interface RootState {

}

export const modules = {
    [student.name]: student,
    [semester.name]: semester,
    [course.name]: course
};
