import {lookup, StrMap} from "fp-ts/lib/StrMap";
import {fromArray, NonEmptyArray} from "fp-ts/lib/NonEmptyArray";
import {curry, flip} from "fp-ts/lib/function";
import {Option} from "fp-ts/lib/Option";

export namespace DayService {
    // noinspection NonAsciiCharacters
    export const DAY_CHINESE_TO_NUMBER = new StrMap<number>({
        '日': 0,
        '一': 1,
        '二': 2,
        '三': 3,
        '四': 4,
        '五': 5,
        '六': 6
    });

    export const DAY_NUMBER_TO_CHINESE = fromArray(['日', '一', '二', '三', '四', '五', '六']).toNullable() as NonEmptyArray<string>;

    export function dayChineseToNumber(chinese: string): Option<number> {
        return lookup(chinese, DAY_CHINESE_TO_NUMBER);
    }

    export const dayNumberToChinese = DAY_NUMBER_TO_CHINESE.index.bind(DAY_NUMBER_TO_CHINESE);
}