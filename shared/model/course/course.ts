import {Class} from "./class/class";

export interface Course {
    readonly id: string;
    readonly name: string;
    readonly teacherId: any;
    readonly semesterId: any;
    readonly classes: Array<Class>;
    readonly place: string;
}

