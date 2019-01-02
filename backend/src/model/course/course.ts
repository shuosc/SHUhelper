import {Teacher, TeacherRepository} from "../teacher";
import {ObjectID} from "bson";
import {redis} from "../../infrastructure/redis";
import {mongodb} from "../../infrastructure/mongodb";
import {Semester, SemesterRepository} from "../semester/semester";
import {assert} from "../../../../shared/tools/assert";
import {CourseTime} from "../../../../shared/model/courseTime";

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
        const semester = await SemesterRepository.getById(new ObjectID(rawObject['semesterId']));
        const teacher = await TeacherRepository.getById(new ObjectID(rawObject['teacherId']));
        assert(semester !== null);
        assert(teacher !== null);
        return new Course(
            new ObjectID(rawObject['_id']),
            rawObject['id'],
            rawObject['name'],
            semester,
            teacher,
            rawObject['multipleTeacher'],
            rawObject['time'].map(CourseTime.fromRawObject),
            rawObject['place']
        );
    }

    static async fromJson(json: JSON): Promise<Course> {
        assert(json['semesterId'] !== null);
        assert(json['teacherId'] !== null);
        return this.fromRawObject(json);
    }

    serialize() {
        assert(this.semester !== null);
        assert(this.teacher !== null);
        assert(this._id instanceof ObjectID);
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
        assert(rawObject.teacherId !== null);
        let course = await Course.fromRawObject(rawObject);
        await cache(course);
        return course;
    }

    export async function save(object: Course) {
        await TeacherRepository.save(object.teacher);
        await SemesterRepository.save(object.semester);
        const cachePromise = cache(object);
        const mongodbPromise = mongodb.collection('course').updateOne({_id: object._id}, {$set: object.serialize()}, {upsert: true});
        await Promise.all([cachePromise, mongodbPromise]);
    }

    export async function count(): Promise<number> {
        return await mongodb.collection('course').countDocuments();
    }
}