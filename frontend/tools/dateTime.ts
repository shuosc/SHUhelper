const dateRegex = /((\d{4})|([+-]?\d{6}))-(\d{2})-(\d{2})T\d{2}:\d{2}:\d{2}\.\d{3}Z/;

export function createTime(hours: number, minutes: number, seconds = 0): Date {
    return new Date(0, 0, 0, hours, minutes, seconds);
}

export function createDate(year: number, month: number, day: number): Date {
    return new Date(year, month - 1, day);
}

export function mergeDateTime(date: Date, time: Date) {
    return new Date(date.getFullYear(), date.getMonth(), date.getDate(),
        time.getHours(), time.getMinutes(), time.getSeconds());
}

export function extractTime(dateTime: Date): Date {
    return createTime(dateTime.getHours(), dateTime.getMinutes(), dateTime.getSeconds());
}

export function normalizeDateTimeInObject(object: any): any {
    if (typeof object === "string") {
        if (dateRegex.test(object)) {
            return new Date(object);
        } else {
            return object;
        }
    } else if (typeof object === "object") {
        if (object instanceof Array) {
            return object.map(normalizeDateTimeInObject);
        } else if (object instanceof Date) {
            return new Date(object);
        } else if (object instanceof Object) {
            let result = {};
            for (let attr in object) {
                if (object.hasOwnProperty(attr)) {
                    (result as any)[attr] = normalizeDateTimeInObject(object[attr]);
                }
            }
            return result;
        }
    } else {
        return object;
    }
    throw new Error(`Cannot normalize ${object}!`);
}