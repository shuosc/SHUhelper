import {Document, model, Model, Schema} from 'mongoose';
import * as sharedCourseData from '../../../shared/model/course';
import {SemesterSchema} from './semester';

export interface IClassTime extends Document, sharedCourseData.IClassTime {
}

export function serializeClassTime(classTime: sharedCourseData.IClassTime) {
    return {
        day: classTime.day,
        startSector: classTime.startSector,
        endSector: classTime.endSector
    }
}

export interface IClassLocation extends Document, sharedCourseData.IClassLocation {
}

export function serializeClassLocation(classLocation: sharedCourseData.IClassLocation) {
    return {
        campus: classLocation.campus,
        building: classLocation.building,
        roomNumber: classLocation.roomNumber
    }
}

export interface IClass extends Document, sharedCourseData.IClass {

}

export function serializeClass(class_: IClass) {
    return {
        time: serializeClassTime(class_.time),        // 上课时间
        location: serializeClassLocation(class_.location), // 上课所在的位置
        type: class_.type           // 课程类型
    }
}

export interface ICourse extends Document, sharedCourseData.ICourse {
    id: string
}

export function serializeCourse(course: ICourse) {
    return {
        id: course.id,
        name: course.name,
        teacher: course.teacher.id,
        manyTeacher: course.manyTeacher,
        semester: course.semester.id,
        classes: course.classes.map(serializeClass)
    }
}

export const ClassTimeSchema: Schema = new Schema({
    day: {type: Number, required: true},
    startSector: {type: Number, required: true},
    endSector: {type: Number, required: true}
});

export const ClassLocationSchema: Schema = new Schema({
    campus: {type: String, required: true},
    building: {type: String, required: true},
    roomNumber: {type: String}
});

export const ClassSchema: Schema = new Schema({
    time: {type: ClassTimeSchema, required: true},          // 上课时间
    location: {type: ClassLocationSchema, required: true},  // 上课所在的位置
    type: {type: Number, required: true}                    // 课程类型
});

export const CourseSchema: Schema = new Schema({
    id: {type: String, required: true},
    name: {type: String, required: true},
    teacher: {type: String, required: true},
    manyTeacher: {type: Boolean, required: true},
    semester: {type: SemesterSchema, required: true},
    classes: {type: [ClassSchema], required: true}
});

export const Course: Model<ICourse> = model('Course', CourseSchema);