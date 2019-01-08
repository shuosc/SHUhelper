import {ObjectID} from "mongodb";
import {mongo, removeId} from "../../infrastructure/mongo";
import {redis} from "../../infrastructure/redis";
import * as fs from "fs";
import {Semester, SemesterService} from "../../../../shared/model/semester/semester";
import {DateRangeService} from "../../../../shared/model/dateRange/dateRange";
import {assert} from "../../../../shared/tools/assert";

export namespace SemesterRepository {
    let currentSemester: Semester = null;

    async function cache(object: Semester) {
        let data = JSON.stringify(object);
        await redis.set('semester_' + object._id, data);
    }

    export async function getById(id: ObjectID | string): Promise<Semester | null> {
        if (typeof id === 'string') {
            id = new ObjectID(id);
        }
        const objectInBuffer = await redis.get('semester_' + id);
        if (objectInBuffer !== null) {
            return JSON.parse(objectInBuffer);
        }
        const semester: Semester = await mongo.collection('semester').findOne({_id: id});
        if (semester === null)
            return null;
        await cache(semester);
        assert(semester.begin instanceof Date);
        return semester;
    }

    export async function getByName(name: string): Promise<Semester | null> {
        return await mongo.collection('semester').findOne({name: name});
    }

    /**
     * 当前学期
     */
    export async function current(): Promise<Semester | null> {
        const now = new Date();
        if (currentSemester === null || !DateRangeService.isDateIn(currentSemester, now)) {
            currentSemester = await mongo.collection('semester').findOne({
                begin: {$lte: now},
                end: {$gt: now}
            });
        }
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
            semester._id = new ObjectID();
            semester = SemesterService.normalize(semester);
            await SemesterRepository.save(semester);
        }
    }
}