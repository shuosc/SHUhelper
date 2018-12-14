/**
 * 假期
 * 表示在 [begin,end] 时间区间内都可以休息
 */
export interface IHoliday {
  name: string;
  begin: Date;                // 假期开始日，时间为全0
  end: Date;                  // 假期结束日，时间为全最大值
}

/**
 * 调休
 */
export interface IHolidayWithShift extends IHoliday {
  shiftMap: Map<Date, Date>;  // 调休后补工作日->原工作日的map
}

/**
 * 判断一个 IHoliday 是否有调休
 * @param holiday 要判断的 IHoliday
 */
function hasShift(holiday: IHoliday): holiday is IHolidayWithShift {
  return (holiday as IHolidayWithShift).shiftMap !== undefined;
}

/**
 * 一个学期
 */
export interface ISemester {
  id: string;
  name: string;
  begin: Date;                // 开始日期，必须是一个周一，时间为全0
  end: Date;                  // 结束日期，必须是一个周日，时间为全最大值
  holidays: Array<IHoliday>;  // 学期中的假期
}