import {Course} from "../../../../shared/model/course/course";
import {redis} from "../../infrastructure/redis";
import {mongo} from "../../infrastructure/mongo";

export namespace CourseRepository {
    async function cache(object: Course) {
        let data = JSON.stringify(object);
        await redis.set('course_' + object.id, data);
    }

    export async function getById(id: string): Promise<Course | null> {
        let objectInBuffer = await redis.get('course_' + id);
        if (objectInBuffer !== null) {
            return JSON.parse(objectInBuffer);
        }
        return await mongo.collection('course').findOne({id: id});
    }

    export async function save(object: Course) {
        const cachePromise = cache(object);
        const mongodbPromise = mongo.collection('course').updateOne({id: object.id}, {$set: object}, {upsert: true});
        await Promise.all([cachePromise, mongodbPromise]);
    }

    export async function count(): Promise<number> {
        return await mongo.collection('course').countDocuments();
    }
}