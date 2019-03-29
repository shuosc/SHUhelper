import {ObjectID} from "mongodb";
import {mongo, removeId} from "../../infrastructure/mongo";
import {redis, RedisService} from "../../infrastructure/redis";
import {fromNullable, none, Option} from "fp-ts/lib/Option";
import {Semester} from "../../../../shared/model/semester/semester";
import {partial} from "../../../tools/partial";
import {normalizeDateTimeInObject} from "../../../tools/dateTime";


export namespace SemesterRepository {
    let currentSemester: Option<Semester> = none;

    const cache = partial(RedisService.cache, 'semester');

    export async function getById(id: ObjectID | string): Promise<Option<Semester>> {
        if (typeof id === 'string') {
            id = new ObjectID(id);
        }
        const objectInBuffer = fromNullable(await redis.get('semester_' + id));
        if (!objectInBuffer.isNone()) {
            return objectInBuffer.map(JSON.parse);
        }
        const semester: Option<Semester> = fromNullable(await mongo.collection('semester').findOne({_id: id}));
        semester.map(cache);
        return semester;
    }

    export async function getByName(name: string): Promise<Option<Semester>> {
        return fromNullable(await mongo.collection('semester').findOne({name: name}));
    }

    export async function getByDate(date: Date): Promise<Option<Semester>> {
        return fromNullable(await mongo.collection('semester').findOne({
            start: {$lte: date},
            end: {$gt: date}
        }));
    }

    /**
     * 当前学期
     */
    export async function current(): Promise<Option<Semester>> {
        if (currentSemester.isNone()) {
            currentSemester = await getByDate(new Date());
        }
        return currentSemester;
    }

    export async function save(object: Semester) {
        object = normalizeDateTimeInObject(JSON.parse(JSON.stringify(object)));
        if (object._id === null) {
            await mongo.collection('semester').insertOne(object);
        } else {
            const cachePromise = cache(object);
            const mongodbPromise = mongo.collection('semester').updateOne({_id: new ObjectID(object._id)}, {$set: removeId(object)}, {upsert: true});
            await Promise.all([cachePromise, mongodbPromise]);
        }
    }

    export async function all(): Promise<Array<Semester>> {
        let cursor = mongo.collection('semester').find();
        let result = [];
        await cursor.forEach((thisSemester) => {
            result.push(thisSemester);
        });
        return result;
    }

    export async function remove(id: ObjectID) {
        await mongo.collection('semester').deleteOne({_id: id});
    }
}
