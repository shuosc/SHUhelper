import 'mocha';
import {simulateLogin} from '../../simulateLogin/simulateLogin';
import {expect} from 'chai';
import {Cookie} from "tough-cookie";
import {fetchCoursePage, parseCoursePage} from "./courseTable";
import * as fs from "fs";
import {initDB, mongo} from "../../../infrastructure/mongo";
import {CourseRepository} from "../../../model/course/course";
import {initSemesters} from "../../../model/semester/semester";
import {redis} from "../../../infrastructure/redis";

describe('爬取课表测试', async () => {
    it('能爬到课表页面', async () => {
        let cookies = await simulateLogin('http://xk.autoisp.shu.edu.cn', process.env.STUDENT_ID, process.env.PASSWORD);
        cookies = [Cookie.fromJSON(cookies[0].toJSON())];
        const coursePage = await fetchCoursePage(process.env.STUDENT_ID, cookies);
        expect(coursePage.indexOf('学号：&nbsp;&nbsp;&nbsp;' + process.env.STUDENT_ID)).not.equal(-1);
    });
    it('能parse课表页面', async () => {
        await initDB();
        await initSemesters();
        await redis.flushall();
        await mongo.collection('course').deleteMany({});
        await mongo.collection('teacher').deleteMany({});
        let coursePage = fs.readFileSync('./src/service/crawl/courseTable/coursePageExample.html').toString();
        let courses = await parseCoursePage(coursePage);
        await Promise.all(courses.map(async (it) => CourseRepository.save(it)));
        expect((await CourseRepository.getById('00853521'))._id).not.equals(null);
        expect((await CourseRepository.getById('00853521')).name).equals('高尔夫球(2)');
        expect((await CourseRepository.getById('00853521')).teacher.name).equals('沙俊波');
        expect((await CourseRepository.getById('1200L018')).multipleTeacher).true;
        await redis.flushall();
        courses = await parseCoursePage(coursePage);
        await Promise.all(courses.map(async (it) => CourseRepository.save(it)));
        expect(await CourseRepository.count()).equals(14);
    });
});