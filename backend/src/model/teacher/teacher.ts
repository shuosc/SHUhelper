import {Teacher as SharedTeacher} from "../../../../shared/model/teacher/teacher";
import {ObjectID} from "mongodb";
import {redis} from "../../infrastructure/redis";
import {mongo} from "../../infrastructure/mongo";

export interface Teacher extends SharedTeacher {
    _id: ObjectID;
}


export namespace TeacherRepository {
    async function cache(object: Teacher) {
        let data = JSON.stringify(object);
        await redis.set('teacher_' + object._id, data);
    }

    export async function getById(id: string | ObjectID): Promise<Teacher | null> {
        const objectId = new ObjectID(id);
        let objectInBuffer = await redis.get('teacher_' + objectId);
        if (objectInBuffer !== null) {
            return JSON.parse(objectInBuffer);
        }
        return await mongo.collection('teacher').findOne({_id: objectId});
    }

    export async function save(object: Teacher) {
        const cachePromise = cache(object);
        const mongodbPromise = mongo.collection('teacher').updateOne({_id: object._id}, {$set: object}, {upsert: true});
        await Promise.all([cachePromise, mongodbPromise]);
    }

    export async function count(): Promise<number> {
        return await mongo.collection('teacher').countDocuments();
    }

    export async function getOrCreateByName(name: string) {
        let teacher = await mongo.collection('teacher').findOne({name: name});
        if (teacher === null) {
            teacher = {
                _id: new ObjectID(),
                name: name
            };
            await mongo.collection('teacher').insertOne(teacher);
        }
        await cache(teacher);
        return teacher;
    }
}