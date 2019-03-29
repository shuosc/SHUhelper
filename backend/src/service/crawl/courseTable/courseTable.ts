import {Cookie} from 'tough-cookie';
import {postFormWithCookies} from '../../../infrastructure/request';
import * as Cheerio from 'cheerio';
import {ClassService} from "../../../../../shared/model/course/class/class";
import {CourseRepository} from "../../../model/course/course";
import {XmlEntities} from "html-entities";
import {TeacherRepository} from "../../../model/teacher/teacher";
import {Course} from "../../../../../shared/model/course/course";
import {SemesterRepository} from "../../../model/semester/semester";
import * as _ from "lodash";
import {Maybe} from "../../../../../shared/tools/functools/maybe";
import {LabClass} from "../../../../../shared/model/course/class/labClass";

const entities = new XmlEntities();

/**
 * 下载课程页面
 */
export function fetchCoursePage(studentId: string, cookies: Array<Cookie>): Promise<string> {
    return postFormWithCookies(cookies, 'http://xk.autoisp.shu.edu.cn:8080/StudentQuery/CtrlViewQueryCourseTable', {
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
async function parseCourse(cols: Array<string>): Promise<Maybe<Course>> {
    const id = cols[1] + '_' + cols[3];
    let result = await CourseRepository.getById(cols[1]);
    if (!result.isNull) {
        return result;
    }
    const name = cols[2];
    const hasManyTeacher = cols[4][cols[4].length - 1] === '等';
    const teacher = await TeacherRepository.getOrCreateByName(hasManyTeacher ? cols[4].slice(0, -1) : cols[4]);
    const semester = await SemesterRepository.current();
    const classFromString = _.partial(ClassService.fromString, _, id);
    const classes = (await parseClassStrings(cols[6]))
        .map(classFromString)
        .filter(it => it.value !== null)
        .map(it => it.value);
    const place = await cols[7];
    return semester.map(semester => {
        return {
            id: id,
            name: name,
            teacherId: teacher._id,
            semesterId: semester._id,
            classes: classes,
            place: place
        }
    });
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
        await course.map(CourseRepository.save).value;
        if (!course.isNull) {
            courses.push(course.value);
        }
    }
    return courses;
}

export function fetchLabCourseListPage(): string {
    let url:string = 'https://www.phylab.shu.edu.cn/openexp/index.php/Public/clist';
    //Need login first
    //After finishing auth module, just get from this url
    //below is an example return value
    return "<html><head></head><body><table id=\"checkList\" class=\"list\" cellpadding=\"0\" cellspacing=\"0\"><tbody><tr><td colspan=\"6\" bgcolor=\"#00008B\"></td></tr><tr class=\"row\"><th colspan=\"6\" class=\"space\">我的课程</th></tr><tr class=\"row\"><td>窗口</td><td>课程号</td><td>教师号</td><td>实验</td><td>学期</td></tr><tr class=\"row\"><td>[二1-2]</td><td>01034120=&gt;大类一</td><td>1052</td><td><table width=\"100%\"><tbody><tr><td>周</td><td>名称</td><td>座位号</td><td>房间</td></tr><tr><td>1</td><td>基础</td><td></td><td>按选课指定教室</td></tr><tr><td>2</td><td>基础</td><td></td><td>按选课指定教室</td></tr><tr><td>3</td><td>基础</td><td></td><td>按选课指定教室</td></tr><tr><td>4</td><td>预习</td><td>第一节：7<br>第二节：7</td><td>第一节：F101<br>第二节：F102</td></tr><tr><td>5</td><td>霍尔法测磁场</td><td>7</td><td>F101</td></tr><tr><td>6</td><td>静电场描绘</td><td>7</td><td>F102</td></tr><tr><td>7</td><td>预习</td><td>第一节：10<br>第二节：10</td><td>第一节：F105<br>第二节：F105</td></tr><tr><td>8</td><td>电位差计使用</td><td>10</td><td>F105</td></tr><tr><td>9</td><td>粘滞系数的测定</td><td>10</td><td>F105</td></tr><tr><td>10</td><td>考核</td><td></td><td>大屏幕公布</td></tr></tbody></table><form id=\"form1\" name=\"form1\" method=\"post\" action=\"http://pmedia.shu.edu.cn/xiti/index.aspx\" target=\"_blank\"><input type=\"hidden\" name=\"cid\" value=\"01034120\"><input type=\"hidden\" name=\"sid\" value=\"18122560\"><input type=\"hidden\" name=\"tno\" value=\"1052\"><input type=\"hidden\" name=\"tt\" value=\"二1-2\"><input type=\"hidden\" name=\"name\" value=\"古彧滔\"><input type=\"submit\" name=\"submit1\" value=\"基础知识习题\"></form></td><td>18-19冬季</td></tr><input type=\"hidden\" name=\"__hash__\" value=\"8a0a461cad2573ba9ea84a4d75256ae6_94b14669a20a68f069450f6a21799aa1\"></tbody></table></body></html>";
}

export function parseLabCourse(cols: Array<string>): LabClass {
    return {
        experiment: cols[1],
        room: cols[3].replace("<br>", "/"),
        week: Number(cols[0].trim())
    };
}

export async function getPhysicsLabCourse(labCourseListPage: string): Promise<Array<LabClass>> {
    let classes: Array<LabClass> = [];
    let $ = Cheerio.load(labCourseListPage, {ignoreWhitespace: true});
    const rows = $("table table tr");

    for(let i = 1; ; i++) {
        const row = $(rows[i]);
        let cols = [];
        row.find('td').each((_, element: CheerioElement) => {
            cols.push(entities.decode($(element).html()));
        });

        if(cols.length !== 4) break;

        let labClass = parseLabCourse(cols);
        if(labClass != null) {
            classes.push(labClass);
        }
    }

    return classes;

}