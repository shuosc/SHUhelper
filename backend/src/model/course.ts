import {ObjectID} from "bson";
import {Teacher} from "./teacher";

export class CourseTime {
    day: number;
    beginSector: number;
    endSector: number;
}

export class Course {
    constructor(
        readonly _id: ObjectID, // mongodb 的 id
        readonly id: string,    // 教务系统中的id
        public name: string,
        public teacher: Teacher,
        public multipleTeacher: boolean,
        public time: Array<CourseTime>,
        public place: Array<string>
    ) {
    }
}