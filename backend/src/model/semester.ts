import { Document, model, Model, Schema } from 'mongoose';
import * as sharedSemester from '../../../shared/model/semester';
import * as fs from 'fs';

export interface IHoliday extends Document, sharedSemester.IHoliday {

}

export interface IHolidayWithShift extends Document, sharedSemester.IHolidayWithShift {
}

export interface ISemester extends Document, sharedSemester.ISemester {
  id: string
}

export const HolidaySchema: Schema = new Schema({
  name: { type: String, required: true },
  begin: { type: Date, required: true },
  end: { type: Date, required: true }
});

export const HolidayWithShiftSchema: Schema = new Schema({
  begin: { type: Date, required: true },
  end: { type: Date, required: true },
  map: { type: Map, from: Date, to: Date, required: true }
});

export const SemesterSchema: Schema = new Schema({
  id: { type: String, required: true },
  name: { type: String, required: true },
  begin: { type: Date, required: true },
  end: { type: Date, required: true },
  holidays: [HolidaySchema]
});

export const Semester: Model<ISemester> = model('Semester', SemesterSchema);

/**
 * 从 semester.json 加载学期信息
 * todo: 实现后台管理页面后，将不再从json文件加载信息
 */
export async function initSemester() {
  const semesterJson = JSON.parse(fs.readFileSync('./initialData/semester.json').toString());
  for (let semester of semesterJson.semester) {
    let model = await Semester.findOne({ id: semester.id }).exec();
    if (model === null) {
      model = new Semester({
        id: semester.id,
        name: semester.name,
        begin: new Date(semester.begin[0], semester.begin[1] - 1, semester.begin[2]),
        end: new Date(semester.end[0], semester.end[1] - 1, semester.end[2]),
        holidays: [
          ...semester.holiday.map((holidayJson: any) => {
            return {
              name: holidayJson.name,
              begin: new Date(holidayJson.begin[0], holidayJson.begin[1] - 1, holidayJson.begin[2]),
              end: new Date(holidayJson.end[0], holidayJson.end[1] - 1, holidayJson.end[2])
            };
          })
        ]
      });
      await model.save();
    }
  }
}

export async function currentSemester(): Promise<ISemester> {
  return Semester.findOne().$where(function() {
    const today = new Date();
    return this.begin <= today && today <= this.end;
  }).exec();
}