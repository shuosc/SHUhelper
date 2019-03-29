import {redis} from "../../infrastructure/redis";
import {Cookie} from "tough-cookie";
import {fetchCoursePage, getCoursesFromPage, getStudentNameFromPage} from "../../service/crawl/courseTable/courseTable";
import {simulateLogin} from "../../service/simulateLogin/simulateLogin";
import {Student as SharedStudent} from "../../../../shared/model/student/student";
import {fromNullable, none, Option, some} from "fp-ts/lib/Option";

export interface Student extends SharedStudent {
    readonly xkCookie: Cookie;
    readonly courseIds: Array<string>;
}

// 学生的相关信息暂时没有准备放入数据库，仅存在redis中
// 学生到所选课程的关系如何建模、是否保存仍待考虑
// 日后可能有入库的必要
export namespace StudentRepository {
    export async function getById(id: string): Promise<Option<Student>> {
        let result = fromNullable(await redis.get('student_' + id));
        return result.map(JSON.parse);
    }

    export async function save(object: Student) {
        let data = JSON.stringify(object);
        await redis.set('student_' + object.id, data);
    }
}

export namespace StudentService {
    export async function login(studentId: string, password: string): Promise<Option<Student>> {
        let cookie: Array<Cookie>;
        try {
            cookie = await simulateLogin('http://xk.autoisp.shu.edu.cn:8080', studentId, password);
        } catch (e) {
            return none;
        }
        if (cookie.length === 0) {
            return none;
        }
        let student = await StudentRepository.getById(studentId);
        if (student.isSome()) {
            return student;
        }
        const coursePage = await fetchCoursePage(studentId, cookie);
        const name = await getStudentNameFromPage(coursePage);
        const courses = await getCoursesFromPage(coursePage);
        student = some({
            id: studentId,
            name: name,
            xkCookie: cookie[0],
            courseIds: courses.map(it => it.id)
        });
        await student.map(StudentRepository.save).toNullable();
        return student;
    }
}
