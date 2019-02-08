import {ObjectID} from "mongodb";
import {mongo, removeId} from "../../infrastructure/mongo";
import {redis} from "../../infrastructure/redis";
import {Semester} from "../../../../shared/model/semester/semester";
import {DateRangeService} from "../../../../shared/model/dateRange/dateRange";
import {just, Maybe} from "../../../../shared/tools/functools/maybe";
import * as _ from "lodash";
import {DateTimeService} from "../../../../shared/tools/dateTime/dateTime";


export namespace SemesterRepository {
    let currentSemester: Maybe<Semester> = just(null);

    async function cache(object: Semester) {
        let data = JSON.stringify(object);
        await redis.set('semester_' + object._id, data);
    }

    export async function getById(id: ObjectID | string): Promise<Maybe<Semester>> {
        if (typeof id === 'string') {
            id = new ObjectID(id);
        }
        const objectInBuffer = just(await redis.get('semester_' + id));
        if (!objectInBuffer.isNull) {
            return objectInBuffer.map(JSON.parse);
        }
        const semester: Maybe<Semester> = just(await mongo.collection('semester').findOne({_id: id}));
        if (semester === null)
            return null;
        semester.map(cache);
        return semester;
    }

    export async function getByName(name: string): Promise<Maybe<Semester>> {
        return just(await mongo.collection('semester').findOne({name: name}));
    }

    /**
     * 当前学期
     */
    export async function current(): Promise<Maybe<Semester>> {
        const isNowIn = _.partial(DateRangeService.isDateIn, _, DateTimeService.now());
        if (currentSemester.map(isNowIn).value) {
            return currentSemester;
        }
        currentSemester = just(await mongo.collection('semester').findOne({
            begin: {$lte: DateTimeService.now()},
            end: {$gt: DateTimeService.now()}
        }));
        return currentSemester;
    }

    export async function save(object: Semester) {
        if (object._id === null) {
            await mongo.collection('semester').insertOne(object);
        } else {
            const cachePromise = cache(object);
            const mongodbPromise = mongo.collection('semester').updateOne({_id: object._id}, {$set: removeId(object)}, {upsert: true});
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
