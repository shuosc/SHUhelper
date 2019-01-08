import {Course} from "../../../../shared/model/course/course";
import {redis} from "../../infrastructure/redis";
import {mongo, removeId} from "../../infrastructure/mongo";

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
        let alreadyInDB = await mongo.collection('course').findOne({id: object.id});
        let mongodbPromise: Promise<any>;
        if (alreadyInDB === null) {
            mongodbPromise = mongo.collection('course').insertOne(object);
        } else {
            mongodbPromise = mongo.collection('course').updateOne({id: object.id}, {$set: removeId(object as any)}, {upsert: true});
        }
        await Promise.all([cachePromise, mongodbPromise]);
    }

    export async function count(): Promise<number> {
        return await mongo.collection('course').countDocuments();
    }
}
