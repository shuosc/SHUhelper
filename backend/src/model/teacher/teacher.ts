import {ObjectID} from "mongodb";
import {redis, RedisService} from "../../infrastructure/redis";
import {mongo, removeId} from "../../infrastructure/mongo";
import {fromNullable, Option} from "fp-ts/lib/Option";
import {partial} from "../../../tools/partial";
import {Teacher} from "../../../../shared/model/teacher/teacher";


export namespace TeacherRepository {
    const cache = partial(RedisService.cache, 'course');

    export async function getById(id: string | ObjectID): Promise<Option<Teacher>> {
        let objectId = new ObjectID(id);
        let objectInBuffer = fromNullable(await redis.get('teacher_' + objectId));
        if (objectInBuffer.isNone()) {
            return objectInBuffer.map(JSON.parse);
        }
        return fromNullable(await mongo.collection('teacher').findOne({_id: objectId}));
    }

    export async function save(object: Teacher) {
        const cachePromise = cache(object);
        const mongodbPromise = mongo.collection('teacher').updateOne({_id: object._id}, {$set: removeId(object)}, {upsert: true});
        await Promise.all([cachePromise, mongodbPromise]);
    }

    export async function getOrCreateByName(name: string): Promise<Teacher> {
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