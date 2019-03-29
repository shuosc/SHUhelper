export interface Class {
    readonly day: number;           // 周几的课
    readonly courseId: any;         // 所属课程
    readonly beginSector: number;   // 在第几节开始
    readonly endSector: number;     // 在第几节结束
    readonly weeks: Array<number>;  // 哪几周有这个课
}

