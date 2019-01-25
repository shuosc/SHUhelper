import {Course} from "../../../../shared/model/course/course";
import {redis} from "../../infrastructure/redis";
import {mongo, removeId} from "../../infrastructure/mongo";
import {ObjectID} from "bson";
import {just, Maybe} from "../../../../shared/tools/functools/maybe";

export namespace CourseRepository {
    async function cache(object: Course) {
        let data = JSON.stringify(object);
        await redis.set('course_' + object.id, data);
    }

    export async function getById(id: string): Promise<Maybe<Course>> {
        let objectInBuffer = just(await redis.get('course_' + id));
        if (!objectInBuffer.isNull) {
            return objectInBuffer.map(JSON.parse);
        }
        return just(await mongo.collection('course').findOne({id: id}));
    }

    export async function save(object: Course) {
        let newObject = {
            ...object
        };
        newObject.semesterId = (object.semesterId as ObjectID).toHexString();
        newObject.teacherId = (object.teacherId as ObjectID).toHexString();
        const cachePromise = cache(newObject);
        let alreadyInDB = await mongo.collection('course').findOne({id: newObject.id});
        let mongodbPromise: Promise<any>;
        if (alreadyInDB === null) {
            mongodbPromise = mongo.collection('course').insertOne({_id: new ObjectID(), ...newObject});
        } else {
            mongodbPromise = mongo.collection('course').updateOne({_id: (newObject as any)._id}, {$set: removeId(newObject as any)}, {upsert: true});
        }
        await Promise.all([cachePromise, mongodbPromise]);
    }

    export async function count(): Promise<number> {
        return await mongo.collection('course').countDocuments();
    }
}
