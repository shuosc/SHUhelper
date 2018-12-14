import * as sharedTeacherData from '../../../shared/model/teacher';
import { Document, model, Model, Schema } from 'mongoose';

export interface ITeacher extends Document, sharedTeacherData.ITeacher {
}

export const TeacherSchema: Schema = new Schema({
  name: { type: String, required: true }
});

export const Teacher: Model<ITeacher> = model('Teacher', TeacherSchema);

export async function getOrCreateTeacherByName(name: string): Promise<ITeacher> {
  let result = await Teacher.findOne({ name: name }).exec();
  if (result === null) {
    result = await Teacher.create({
      name: name
    });
    result = await result.save();
  }
  return result;
}