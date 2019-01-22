import {Cookie} from 'tough-cookie';
import {postFormWithCookies} from '../../../infrastructure/request';
import * as Cheerio from 'cheerio';
import {ClassService} from "../../../../../shared/model/course/class/class";
import {CourseRepository} from "../../../model/course/course";
import {XmlEntities} from "html-entities";
import {TeacherRepository} from "../../../model/teacher/teacher";
import {Course} from "../../../../../shared/model/course/course";
import {SemesterRepository} from "../../../model/semester/semester";

const entities = new XmlEntities();

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

/**
 * 从字符串中解析出所有课
 */
export async function parseClassStrings(str: string): Promise<Array<string>> {
    const regex = /[一二三四五六日]\d+-\d+([^一二三四五]*)/gm;
    let result = new Array<string>();
    let match;
    do {
        match = regex.exec(str);
        if (match !== null) {
            result.push(match[0]);
        }
    } while (match !== null);
    return result;
}

/**
 * 从爬到的课程表格的一行中解析出课程
 */
async function parseCourse(cols: Array<string>): Promise<Course> {
    const id = cols[1] + '_' + cols[3];
    let result = await CourseRepository.getById(cols[1]);
    if (result !== null) {
        return result;
    }
    const name = cols[2];
    const hasManyTeacher = cols[4][cols[4].length - 1] === '等';
    const teacher = await TeacherRepository.getOrCreateByName(hasManyTeacher ? cols[4].slice(0, -1) : cols[4]);
    const semester = await SemesterRepository.current();
    const classes = (await parseClassStrings(cols[6]))
        .map(it => ClassService.fromString(it, id))
        .filter(it => it.value !== null)
        .map(it => it.value);
    const place = await cols[7];
    return {
        id: id,
        name: name,
        teacherId: teacher._id,
        semesterId: semester._id,
        classes: classes,
        place: place
    };
}

/**
 * 从课程页面中解析出所有课程
 */
export async function getCoursesFromPage(coursePage: string): Promise<Array<Course>> {
    const $ = Cheerio.load(coursePage, {ignoreWhitespace: true});
    const rows = $(".tbllist tr");
    let courses: Array<Course> = [];
    for (let i = 3; ; ++i) {
        const row = $(rows[i]);
        let cols = [];
        row.find('td').each((_, element: CheerioElement) => {
            cols.push(entities.decode($(element).html().trim()));
        });
        if (cols.length !== 11) {
            break;
        }
        let course = await parseCourse(cols);
        await CourseRepository.save(course);
        courses.push(course);
    }
    return courses;
}