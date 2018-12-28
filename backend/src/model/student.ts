import {redis} from "../infrastructure/redis";
import {Cookie} from "tough-cookie";
import {fetchCoursePage, getStudentNameFromPage, parseCoursePage} from "../service/crawl/courseTable/courseTable";
import {Course, CourseRepository} from "./course/course";
import {assert} from "../../../shared/tools/assert";

export class Student {
    constructor(readonly id: string) {
        this.id = id;
    }

    private _name: string = null;

    async getName() {
        if (this._name === null) {
            this._name = getStudentNameFromPage(await fetchCoursePage(this.id, [this.xkCookie]));
        }
        return this._name;
    }

    xkCookie: Cookie;       // 此处命名xk是由于要登录的网站是 xk......
                            // 可以商榷是否改名为courseSelectingCookie等

    private _courses: Array<Course> = null;

    static async fromJson(json: JSON): Promise<Student> {
        let result = new Student(json['id']);
        if (json['name'] === undefined) {
            result._name = null;
        } else {
            result._name = json['name'];
        }
        if (json['xkCookie'] === undefined || json['xkCookie'] === null) {
            result.xkCookie = null;
        } else {
            result.xkCookie = Cookie.fromJSON(json['xkCookie']);
        }
        if (json['courseIds'] === undefined || json['courseIds'] === null) {
            result._courses = null;
        } else {
            let coursePromises: Array<Promise<Course>> = json['courseIds'].map(
                async id => CourseRepository.getById(id)
            );
            result._courses = await Promise.all(coursePromises);
        }
        return result;
    }

    async serialize() {
        return {
            id: this.id,
            name: await this.getName(),
            xkCookie: this.xkCookie.toJSON(),
            courseIds: (await this.getCourses()).map(it => it.id)
        }
    }

    async getCourses(): Promise<Array<Course>> {
        if (this._courses === null) {
            const coursePage = await fetchCoursePage(this.id, [this.xkCookie]);
            this._courses = await parseCoursePage(coursePage);
            await Promise.all(this._courses.map(async it => CourseRepository.save(it)));
            for (let course of this._courses) {
                assert(course !== null);
            }
        }
        for (let course of this._courses) {
            assert(course !== null);
        }
        return this._courses;
    }
}

// 学生的相关信息暂时没有准备放入数据库，仅存在redis中
// 学生到所选课程的关系如何建模、是否保存仍待考虑
// 日后可能有入库的必要
export namespace StudentRepository {
    export async function getById(id: string): Promise<Student> {
        let result = await redis.get('student_' + id);
        if (result === null) {
            return null;
        }
        return await Student.fromJson(JSON.parse(result))
    }

    export async function save(object: Student) {
        let data = JSON.stringify(await object.serialize());
        await redis.set('student_' + object.id, data);
    }
}