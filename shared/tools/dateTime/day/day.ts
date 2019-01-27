import {get, just, Maybe} from "../../functools/maybe";

export namespace DayService {
    export const DAY_CHINESE_TO_NUMBER = new Map<string, number>([
        ['日', 0],
        ['一', 1],
        ['二', 2],
        ['三', 3],
        ['四', 4],
        ['五', 5],
        ['六', 6]
    ]);

    export const DAY_NUMBER_TO_CHINESE = ['日', '一', '二', '三', '四', '五', '六'];

    export function dayChineseToNumber(chinese: string): Maybe<number> {
        return get(DAY_CHINESE_TO_NUMBER, chinese);
    }

    export function dayNumberToChinese(id: number): Maybe<string> {
        return just(DAY_NUMBER_TO_CHINESE[id]);
    }
}