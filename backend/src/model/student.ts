import {redis} from "../infrastructure/redis";
import {Cookie} from "tough-cookie";
import {fetchCoursePage, getStudentNameFromPage} from "../service/crawl/courseTable/courseTable";

export class Student {
    constructor(id: string) {
        this.id = id;
    }

    readonly id: string;

    private _name: string = null;

    async getName() {
        if (this._name === null) {
            this._name = getStudentNameFromPage(await fetchCoursePage(this.id, [this.xkCookie]));
        }
        return this._name;
    }

    xkCookie: Cookie;

    async serialize() {
        return {
            id: this.id,
            name: await this.getName(),
            xkCookie: this.xkCookie.toJSON()
        }
    }

    static fromJson(json: JSON): Student {
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
        return result;
    }
}

export namespace StudentRepository {
    export async function getById(id: string): Promise<Student> {
        let result = await redis.get('student_' + id);
        if (result === null) {
            return null;
        }
        return Student.fromJson(JSON.parse(result))
    }

    export async function save(object: Student) {
        let data = JSON.stringify(await object.serialize());
        await redis.set('student_' + object.id, data);
    }
}