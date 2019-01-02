import {DateRange} from "./dateRange";

export class Holiday {
    constructor(public name: string,
                public dateRange: DateRange) {
    }

    static fromRawObject(rawObject: any): Holiday {
        return new Holiday(
            rawObject['name'],
            DateRange.fromJson(rawObject['dateRange'])
        );
    }

    static fromJson(json: JSON): Holiday {
        return this.fromRawObject(json);
    }

    serialize() {
        return {
            name: this.name,
            dateRange: this.dateRange.serialize()
        };
    }
}