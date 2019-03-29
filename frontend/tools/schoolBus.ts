export interface SchoolBusStation {
    campusId: number,
    startTime?: Date
}

export type SchoolBusRoutine = Array<SchoolBusStation>;


export enum SchoolBusRoutineType {
    WorkingDay = 0,
    NonWorkingDay = 1,
    SummerHoliday = 2
}
