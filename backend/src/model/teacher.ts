import {ObjectID} from "mongodb";
import {redis} from "../infrastructure/redis";
import {mongodb} from "../infrastructure/mongodb";

export class Teacher {
    constructor(
        readonly _id: ObjectID,
        public name: string,
    ) {
    }

    static fromJson(json: JSON): Teacher {
        return new Teacher(json['id'], json['name']);
    }

    static fromRawObject(rawObject) {
        return new Teacher(rawObject['id'], rawObject['name']);
    }

    serialize() {
        return this;
    }
}

export namespace TeacherRepository {
    async function cache(object: Teacher) {
        let data = JSON.stringify(await object.serialize());
        await redis.set('teacher_' + object._id, data);
    }

    export async function getById(id: ObjectID | string): Promise<Teacher | null> {
        if (typeof id === 'string') {
            id = new ObjectID(id);
        }
        let objectInBuffer = await redis.get('teacher_' + id);
        if (objectInBuffer !== null) {
            return Teacher.fromJson(JSON.parse(objectInBuffer));
        }
        const rawObject = await mongodb.collection('teacher').findOne({id: id});
        if (rawObject === null)
            return null;
        let teacher = Teacher.fromRawObject(rawObject);
        await cache(teacher);
        return teacher;
    }

    export async function save(object: Teacher) {
        if (object._id === null) {
            await mongodb.collection('teacher').insertOne(object.serialize());
        } else {
            const cachePromise = cache(object);
            const mongodbPromise = mongodb.collection('teacher').updateOne({_id: object._id}, {$set: object.serialize()}, {upsert: true});
            await Promise.all([cachePromise, mongodbPromise]);
        }
    }
}