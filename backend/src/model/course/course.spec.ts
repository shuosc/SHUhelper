import 'mocha';
import {expect} from 'chai';
import {initDB, mongodb} from "../../infrastructure/mongodb";
import {initSemesters, SemesterRepository} from "../semester/semester";
import {Course, CourseRepository} from "./course";
import {Teacher} from "../teacher";
import {redis} from "../../infrastructure/redis";

describe('课程模型测试', async () => {
    it('能被正确序列化/反序列化', async () => {
        await initDB();
        await initSemesters();
        await redis.flushall();
        await mongodb.collection('course').deleteMany({});
        await mongodb.collection('teacher').deleteMany({});
        let semester = await SemesterRepository.current();
        let teacher = new Teacher(null, 'test');
        let theCourse = new Course(null, '00000000', '测试', semester, teacher, false, [], '测试地点');
        await CourseRepository.save(theCourse);
        await redis.flushall();
        theCourse = await CourseRepository.getById('00000000');
        expect(theCourse.teacher).not.equals(null);
        theCourse.name = '测试2';
        await CourseRepository.save(theCourse);
        expect(await mongodb.collection('course').countDocuments()).equals(1);
    });
});