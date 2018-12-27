import {ObjectID} from "mongodb";
import {redis} from "../infrastructure/redis";
import {mongodb} from "../infrastructure/mongodb";
import {assert} from "../../../shared/tools/assert";

export class Teacher {
    constructor(
        readonly _id: ObjectID,
        public name: string) {
        if (_id === null || _id === undefined) {
            this._id = new ObjectID();
        }
    }

    static fromJson(json: JSON): Teacher {
        return this.fromRawObject(json);
    }

    static fromRawObject(rawObject): Teacher {
        return new Teacher(new ObjectID(rawObject['_id']), rawObject['name']);
    }

    serialize() {
        assert(this._id !== null);
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
        const rawObject = await mongodb.collection('teacher').findOne({_id: id});
        if (rawObject === null)
            return null;
        let teacher = await Teacher.fromRawObject(rawObject);
        await cache(teacher);
        return teacher;
    }

    export async function getOrCreateByName(name: string): Promise<Teacher> {
        const rawObject = await mongodb.collection('teacher').findOne({name: name});
        if (rawObject === null) {
            let teacher = new Teacher((await mongodb.collection('teacher')
                .insertOne({
                    _id: new ObjectID(),
                    name: name
                })).insertedId, name);
            await cache(teacher);
            return teacher;
        }
        let teacher = await Teacher.fromRawObject(rawObject);
        await cache(teacher);
        return teacher;
    }

    export async function save(object: Teacher) {
        const cachePromise = cache(object);
        const mongodbPromise = mongodb.collection('teacher').updateOne({_id: object._id}, {$set: object.serialize()}, {upsert: true});
        await Promise.all([cachePromise, mongodbPromise]);
    }
}