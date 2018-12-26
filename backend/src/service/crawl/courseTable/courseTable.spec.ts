import 'mocha';
import {simulateLogin} from '../../simulateLogin/simulateLogin';
import {expect} from 'chai';
import {Cookie} from "tough-cookie";
import {fetchCoursePage} from "./courseTable";
import * as fs from "fs";

describe('爬取课表测试', async () => {
    it('能爬到课表页面', async () => {
        let cookies = await simulateLogin('http://xk.autoisp.shu.edu.cn', process.env.STUDENT_ID, process.env.PASSWORD);
        cookies = [Cookie.fromJSON(cookies[0].toJSON())];
        const coursePage = await fetchCoursePage(process.env.STUDENT_ID, cookies);
        expect(coursePage.indexOf('学号：&nbsp;&nbsp;&nbsp;' + process.env.STUDENT_ID)).not.equal(-1);
    });
    it('能parse课表页面', async () => {
        // await Semester.deleteMany({}).exec();
        // await initSemester();
        // await Teacher.deleteMany({}).exec();
        // await Course.deleteMany({}).exec();
        const coursePage = fs.readFileSync('./src/service/crawl/courseTable/coursePageExample.html').toString();
        // const courses = await parseCoursePage(coursePage);
        // for (let course of courses) {
        //     await course.save();
        // }
        // let theCourse = await Course.findOne({id: '00853521'}).exec();
        // expect(theCourse.classes[0].time.day).equals(3);
        // expect(theCourse.classes[0].time.startSector).equals(7);
        // expect(theCourse.classes[0].time.endSector).equals(8);
        // expect(theCourse.classes[0].type as ClassType).equals(ClassType.normal);
    });
});