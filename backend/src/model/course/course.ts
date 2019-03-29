import {Course} from "../../../../shared/model/course/course";
import {redis, RedisService} from "../../infrastructure/redis";
import {mongo} from "../../infrastructure/mongo";
import {ObjectID} from "bson";
import {partial} from "../../../tools/partial";
import {fromNullable, Option} from "fp-ts/lib/Option";


export namespace CourseRepository {
    const cache = partial(RedisService.cache, 'course');

    export async function getById(id: string): Promise<Option<Course>> {
        let objectInBuffer = fromNullable(await redis.get('course_' + id));
        if (!objectInBuffer.isNone()) {
            return objectInBuffer.map(JSON.parse);
        }
        return fromNullable(await mongo.collection('course').findOne({id: id}));
    }

    export async function save(object: Course) {
        const cachePromise = cache(object);
        let alreadyInDB = await mongo.collection('course').findOne({id: object.id});
        let mongodbPromise: Promise<any>;
        if (alreadyInDB === null) {
            mongodbPromise = mongo.collection('course').insertOne({_id: new ObjectID(), ...object});
            await Promise.all([cachePromise, mongodbPromise]);
        } else {
            await cachePromise;
        }
    }

    export async function count(): Promise<number> {
        return await mongo.collection('course').countDocuments();
    }
}
