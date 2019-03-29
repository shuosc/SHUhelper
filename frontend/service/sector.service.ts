import {fromArray, NonEmptyArray} from "fp-ts/lib/NonEmptyArray";
import {zip} from "fp-ts/lib/Array";
import {addMinutes, isWithinInterval} from "date-fns";
import {partial} from "~/tools/partial";
import {createTime, extractTime} from "~/tools/dateTime";

export namespace SectorRepository {
    export const sectors = new NonEmptyArray(
        createTime(8, 0), [
            createTime(8, 55),
            createTime(10, 0),
            createTime(10, 55),
            createTime(12, 10),
            createTime(13, 5),
            createTime(14, 10),
            createTime(15, 5),
            createTime(16, 0),
            createTime(16, 55),
            createTime(18, 0),
            createTime(18, 55),
            createTime(19, 40),
        ])
        .map(it => {
            return {start: it, end: addMinutes(it, 45)}
        });

    export const rests = fromArray(zip(sectors.toArray(), sectors.tail)
        .map(it => {
            return {start: it[0].end, end: it[1].start}
        })).getOrElse(null as any) as NonEmptyArray<Interval>;
}

export namespace SectorService {
    export function sectorIndexForTime(dateTime: Date) {
        return SectorRepository.sectors.findIndex(partial(isWithinInterval, extractTime(dateTime)));
    }

    export function restIndexForTime(dateTime: Date) {
        return SectorRepository.rests.findIndex(partial(isWithinInterval, extractTime(dateTime)));
    }

    export function restForTime(dateTime: Date) {
        return SectorRepository.rests.findFirst(partial(isWithinInterval, extractTime(dateTime)));
    }
}
