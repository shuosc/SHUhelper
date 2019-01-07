import {redis} from "../../infrastructure/redis";
import {Cookie} from "tough-cookie";
import {fetchCoursePage, getCoursesFromPage, getStudentNameFromPage} from "../../service/crawl/courseTable/courseTable";
import {simulateLogin} from "../../service/simulateLogin/simulateLogin";
import {Student as SharedStudent} from "../../../../shared/model/student";

export interface Student extends SharedStudent {
    readonly xkCookie: Cookie;
    readonly courseIds: Array<string>;
}

// 学生的相关信息暂时没有准备放入数据库，仅存在redis中
// 学生到所选课程的关系如何建模、是否保存仍待考虑
// 日后可能有入库的必要
export namespace StudentRepository {
    export async function getById(id: string): Promise<Student | null> {
        let result = await redis.get('student_' + id);
        if (result === null) {
            return null;
        }
        return JSON.parse(result);
    }

    export async function save(object: Student) {
        let data = JSON.stringify(object);
        await redis.set('student_' + object.id, data);
    }
}

export namespace StudentService {
    export async function login(studentId: string, password: string): Promise<Student | null> {
        let cookie: Array<Cookie>;
        try {
            cookie = await simulateLogin('http://xk.autoisp.shu.edu.cn', studentId, password);
        } catch (e) {
            return null;
        }
        if (cookie.length === 0) {
            return null;
        }
        let student = await StudentRepository.getById(studentId);
        if (student !== null) {
            return student;
        }
        const coursePage = await fetchCoursePage(studentId, cookie);
        const name = await getStudentNameFromPage(coursePage);
        const courses = await getCoursesFromPage(coursePage);
        student = {
            id: studentId,
            name: name,
            xkCookie: cookie[0],
            courseIds: courses.map(it => it.id)
        };
        await StudentRepository.save(student);
        return student;
    }
}