import { Document, model, Model, Schema } from 'mongoose';
import * as sharedCourseData from '../../../shared/model/course';
import { SemesterSchema } from './semester';

export interface IClassTime extends Document, sharedCourseData.IClassTime {
}

export interface IClassLocation extends Document, sharedCourseData.IClassLocation {
}

export interface IClass extends Document, sharedCourseData.IClass {

}

export interface ICourse extends Document, sharedCourseData.ICourse {
  id: string
}

export const ClassTimeSchema: Schema = new Schema({
  day: { type: Number, required: true },
  startSector: { type: Number, required: true },
  endSector: { type: Number, required: true }
});

export const ClassLocationSchema: Schema = new Schema({
  campus: { type: String, required: true },
  building: { type: String, required: true },
  roomNumber: { type: String }
});

export const ClassSchema: Schema = new Schema({
  time: { type: ClassTimeSchema, required: true },          // 上课时间
  location: { type: ClassLocationSchema, required: true },  // 上课所在的位置
  type: { type: Number, required: true }                    // 课程类型
});

export const CourseSchema: Schema = new Schema({
  id: { type: String, required: true },
  name: { type: String, required: true },
  teacher: { type: String, required: true },
  manyTeacher: { type: Boolean, required: true },
  semester: { type: SemesterSchema, required: true },
  classes: { type: [ClassSchema], required: true }
});

export const Course: Model<ICourse> = model('Course', CourseSchema);
