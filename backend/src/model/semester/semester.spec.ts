import 'mocha';
import {expect} from 'chai';
import {initSemesters, SemesterRepository} from "./semester";
import {initDB, mongodb} from "../../infrastructure/mongodb";
import {redis} from "../../infrastructure/redis";

describe('学期模型测试', async () => {
    it('能被正确初始化', async () => {
        await initDB();
        await mongodb.collection('semester').deleteMany({});
        await redis.flushall();
        await initSemesters();
        expect((await SemesterRepository.current()).name).equals("2018-2019 冬季学期");
    });
});