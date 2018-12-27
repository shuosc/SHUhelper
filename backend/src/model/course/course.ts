import {Teacher, TeacherRepository} from "../teacher";
import {ObjectID} from "bson";
import {redis} from "../../infrastructure/redis";
import {mongodb} from "../../infrastructure/mongodb";
import {DAY_CHINESE_TO_NUMBER} from "../../../../shared/tools/date";
import {Semester, SemesterRepository} from "../semester/semester";
import {assert} from "../../../../shared/tools/assert";

export class CourseTime {
    constructor(public day: number,
                public beginSector: number,
                public endSector: number) {
    }

    static fromRawObject(rawObject): CourseTime {
        return new CourseTime(rawObject['day'], rawObject['beginSector'], rawObject['endSector']);
    }

    static fromString(str: string) {
        const regex = /([一二三四五六日])(\d+)-(\d+)/;
        let result = regex.exec(str);
        return new CourseTime(DAY_CHINESE_TO_NUMBER.get(str[0]), parseInt(result[2]), parseInt(result[3]));
    }

    serialize() {
        return this;
    }
}

export class Course {
    constructor(
        readonly _id: ObjectID, // mongodb中的id
        readonly id: string,    // 教务系统中的id
        public name: string,
        public semester: Semester,
        public teacher: Teacher,
        public multipleTeacher: boolean,
        public time: Array<CourseTime>,
        public place: string
    ) {
        if (_id === null || _id === undefined) {
            this._id = new ObjectID();
        }
        assert(semester !== null);
        assert(teacher !== null);
    }

    static async fromRawObject(rawObject) {
        return new Course(
            rawObject['_id'],
            rawObject['id'],
            rawObject['name'],
            await SemesterRepository.getById(rawObject['semesterId']),
            await TeacherRepository.getById(rawObject['teacherId']),
            rawObject['multipleTeacher'],
            rawObject['time'].map(CourseTime.fromRawObject),
            rawObject['place']
        );
    }

    static async fromJson(json: JSON): Promise<Course> {
        return this.fromRawObject(json);
    }

    serialize() {
        assert(this.semester !== null);
        assert(this.teacher !== null);
        return {
            _id: this._id,
            id: this.id,
            name: this.name,
            semesterId: this.semester._id,
            teacherId: this.teacher._id,
            multipleTeacher: this.multipleTeacher,
            time: this.time.map(it => it.serialize()),
            place: this.place
        }
    }
}

export namespace CourseRepository {
    async function cache(object: Course) {
        let data = JSON.stringify(await object.serialize());
        await redis.set('course_' + object.id, data);
    }

    export async function getById(id: string): Promise<Course | null> {
        let objectInBuffer = await redis.get('course_' + id);
        if (objectInBuffer !== null) {
            return Course.fromJson(JSON.parse(objectInBuffer));
        }
        const rawObject = await mongodb.collection('course').findOne({id: id});
        if (rawObject === null)
            return null;
        let course = await Course.fromRawObject(rawObject);
        await cache(course);
        return course;
    }

    export async function save(object: Course) {
        await TeacherRepository.save(object.teacher);
        await SemesterRepository.save(object.semester);
        const cachePromise = cache(object);
        const mongodbPromise = mongodb.collection('course').updateOne({_id: object._id}, {$set: object}, {upsert: true});
        await Promise.all([cachePromise, mongodbPromise]);
    }

    export async function count(): Promise<number> {
        return await mongodb.collection('course').countDocuments();
    }
}