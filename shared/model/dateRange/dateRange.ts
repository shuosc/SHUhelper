export interface DateRange {
    readonly begin: Date;
    readonly end: Date;
}

export namespace DateRangeService {
    export function isDateIn(dateRange: DateRange, date: Date): boolean {
        return dateRange.begin <= date && date < dateRange.end;
    }
}