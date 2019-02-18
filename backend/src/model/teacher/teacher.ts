import {Teacher as SharedTeacher} from "../../../../shared/model/teacher/teacher";
import {ObjectID} from "mongodb";
import {redis, RedisService} from "../../infrastructure/redis";
import {mongo, removeId} from "../../infrastructure/mongo";
import * as _ from "lodash";

export interface Teacher extends SharedTeacher {
    _id: ObjectID;
}


export namespace TeacherRepository {
    const cache = _.partial(RedisService.cache, 'course');

    export async function getById(id: string | ObjectID): Promise<Teacher | null> {
        let objectId = new ObjectID(id);
        let objectInBuffer = await redis.get('teacher_' + objectId);
        if (objectInBuffer !== null) {
            return JSON.parse(objectInBuffer);
        }
        return await mongo.collection('teacher').findOne({_id: objectId});
    }

    export async function save(object: Teacher) {
        const cachePromise = cache(object);
        const mongodbPromise = mongo.collection('teacher').updateOne({_id: object._id}, {$set: removeId(object)}, {upsert: true});
        await Promise.all([cachePromise, mongodbPromise]);
    }

    export async function count(): Promise<number> {
        return await mongo.collection('teacher').countDocuments();
    }

    export async function getOrCreateByName(name: string) {
        let teacher: Teacher = await mongo.collection('teacher').findOne({name: name});
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