export interface DateRange {
    readonly begin: Date;
    readonly end: Date;
}

export interface DateRangeJson {
    readonly begin: string;
    readonly end: string;
}

export namespace DateRangeService {
    export function isDateIn(dateRange: DateRange, date: Date): boolean {
        return dateRange.begin <= date && date < dateRange.end;
    }

    export function normalize(json: DateRangeJson): DateRange {
        return {
            begin: new Date(json.begin),
            end: new Date(json.end)
        }
    }
}