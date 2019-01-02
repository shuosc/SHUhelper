export class DateRange {
    constructor(public begin: Date, public end: Date) {
    }

    get isNowIn() {
        return this.isDateIn(new Date());
    }

    static fromRawObject(rawObject: { begin: Date, end: Date }): DateRange {
        return new DateRange(new Date(rawObject.begin), new Date(rawObject.end));
    }

    static fromJson(json: JSON): DateRange {
        return this.fromRawObject(json as any);
    }

    isDateIn(date: Date) {
        return this.begin <= date && date < this.end;
    }

    serialize() {
        return {
            begin: new Date(this.begin),
            end: new Date(this.end)
        };
    }
}