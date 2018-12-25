import {Cookie} from 'tough-cookie';
import {postFormWithCookies} from '../../../infrastructure/request';
import * as Cheerio from 'cheerio';

/**
 * 下载课程页面
 */
export function fetchCoursePage(studentId: string, cookies: Array<Cookie>): Promise<string> {
    return postFormWithCookies(cookies, 'http://xk.autoisp.shu.edu.cn/StudentQuery/CtrlViewQueryCourseTable', {
        studentNo: process.env.STUDENT_ID
    });
}

/**
 * 从课程页面中读取学生名字
 */
export function getStudentNameFromPage(coursePage: string) {
    let $ = Cheerio.load(coursePage);
    return $("#showStudent td div:nth-of-type(2)").text().trim().slice(3).trim();
}
