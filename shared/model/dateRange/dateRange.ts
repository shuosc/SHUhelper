/**
 * 日期区间类型
 */
export interface DateRange {
    readonly begin: Date;
    readonly end: Date;
}

/**
 * 日期区间被序列化成 JSON 后的类型
 * todo: 考虑使用遍历对象元素+正则表达式判断字符串格式+new Date来替代
 */
export interface DateRangeJson {
    readonly begin: string;
    readonly end: string;
}

export namespace DateRangeService {
    export function isDateIn(dateRange: DateRange, date: Date): boolean {
        return dateRange.begin <= date && date < dateRange.end;
    }

    /**
     * 将序列化为 json 的 DateRange 转回来
     */
    export function normalize(json: DateRangeJson): DateRange {
        return {
            begin: new Date(json.begin),
            end: new Date(json.end)
        }
    }
}