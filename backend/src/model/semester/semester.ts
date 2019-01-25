import {ObjectID} from "mongodb";
import {mongo, removeId} from "../../infrastructure/mongo";
import {redis} from "../../infrastructure/redis";
import * as fs from "fs";
import {Semester} from "../../../../shared/model/semester/semester";
import {DateRangeService} from "../../../../shared/model/dateRange/dateRange";
import * as dateNormalizer from "date-normalizer";
import {just, Maybe} from "../../../../shared/tools/functools/maybe";
import * as _ from "lodash";
import {DateTimeService} from "../../../../shared/tools/dateTime/dateTime";

const normalizeDateInObject = (dateNormalizer as any)['date-normalizer'].normalizeDateInObject;


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
}


/**
 * 这个函数是临时的
 * 在管理员后台准备好之前将会使用json文件来初始化
 */
export async function initSemesters() {
    const data = fs.readFileSync('./initialData/semester.json');
    const json = JSON.parse(data.toString());
    for (let semester of json['semester']) {
        if ((await SemesterRepository.getByName(semester['name'])) === null) {
            semester = normalizeDateInObject(semester);
            semester._id = new ObjectID();
            await SemesterRepository.save(semester);
        }
    }
}