import 'mocha';
import {expect} from 'chai';
import {initSemesters, SemesterRepository} from "./semester";
import {initDB} from "../../infrastructure/mongodb";

describe('学期模型测试', async () => {
    it('能被正确初始化', async () => {
        await initDB();
        await initSemesters();
        expect((await SemesterRepository.current()).name).equals("2018-2019 冬季学期");
    });
});