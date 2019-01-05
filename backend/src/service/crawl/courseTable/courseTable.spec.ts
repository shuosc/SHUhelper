import 'mocha';
import {expect} from 'chai';
import {Cookie} from "tough-cookie";
import {fetchCoursePage, getStudentNameFromPage} from "./courseTable";
import {simulateLogin} from "../../simulateLogin/simulateLogin";
import * as fs from "fs";

describe('爬取课表测试', async () => {
    it('能爬到课表页面', async () => {
        let cookies = await simulateLogin('http://xk.autoisp.shu.edu.cn', process.env.STUDENT_ID, process.env.PASSWORD);
        cookies = [Cookie.fromJSON(cookies[0].toJSON())];
        const coursePage = await fetchCoursePage(process.env.STUDENT_ID, cookies);
        expect(coursePage.indexOf('学号：&nbsp;&nbsp;&nbsp;' + process.env.STUDENT_ID)).not.equal(-1);
    });
    it('能读取学生名字', async () => {
        const coursePage = fs.readFileSync('./src/service/crawl/courseTable/coursePageExample.html').toString();
        const studentName = getStudentNameFromPage(coursePage);
        expect(studentName).equals("龙方淞");
    });
});