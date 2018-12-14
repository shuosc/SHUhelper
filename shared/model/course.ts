import { ITeacher } from './teacher';
import { ISemester } from './semester';

/**
 * 课时间段 -> 课开始时间
 */
export const SECTOR_TO_TIME = [
  new Date(0, 0, 0, 8, 0, 0),
  new Date(0, 0, 0, 8, 55, 0),
  new Date(0, 0, 0, 10, 0, 0),
  new Date(0, 0, 0, 10, 55, 0),
  new Date(0, 0, 0, 12, 10, 0),
  new Date(0, 0, 0, 13, 5, 0),
  new Date(0, 0, 0, 14, 10, 0),
  new Date(0, 0, 0, 15, 5, 0),
  new Date(0, 0, 0, 16, 0, 0),
  new Date(0, 0, 0, 16, 55, 0),
  new Date(0, 0, 0, 18, 0, 0),
  new Date(0, 0, 0, 18, 55, 0),
  new Date(0, 0, 0, 19, 50, 0)
];

/**
 * 一节课的长度
 */
export const CLASS_DURATION = 45; // minutes

/**
 * 上课时间
 * 表示课在第 [startSector, endSector] 节上
 * 即上课时间是 [SECTOR_TO_TIME[startSector-1], SECTOR_TO_TIME[endSector-1]]
 */
export interface IClassTime {
  day: number,
  startSector: number,
  endSector: number,
}

/**
 * 教室
 * 对于不在教学楼内上的课，整个位置信息都放在building中, roomNumber为null
 */
export interface IClassLocation {
  campus: string,     // 校区
  building: string,   // 楼
  roomNumber: string  // 教室门牌号
}

export enum ClassType {
  normal = 1,           // 正常的课
  discussion = 2,       // 研讨课
  computer = 3          // 上机课
}

/**
 * 课
 */
export interface IClass {
  time: IClassTime,        // 上课时间
  location: IClassLocation, // 上课所在的位置
  type: ClassType           // 课程类型
}

/**
 * 课程
 * Entity
 */
export interface ICourse {
  id: string,
  name: string,
  teacher: ITeacher,
  manyTeacher: boolean,
  semester: ISemester,
  classes: Array<IClass>;
}