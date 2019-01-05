import {CourseTime} from "../courseTime/courseTime";

export interface Course {
    readonly id: any;
    readonly name: string;
    readonly teacherId: any;
    readonly semesterId: any;
    readonly times: Array<CourseTime>;
    readonly place: string;
}
