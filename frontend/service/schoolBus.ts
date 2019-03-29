import {findFirst} from "fp-ts/lib/Array";
import {Option, some} from "fp-ts/lib/Option";
import {Campus} from "../../shared/model/campus/campus";
import {SchoolBusRoutine} from "../../shared/model/schoolBus/schoolBus";
import {assert} from "~/tools/assert";

export namespace SchoolBusService {
    export function hasFromTo(bus: SchoolBusRoutine, from: Campus, to: Campus): boolean {
        assert(from !== to);
        const fromIndex = bus.findIndex(it => it.campusId === from.id);
        const toIndex = bus.findIndex(it => it.campusId === to.id);
        return fromIndex !== -1 && toIndex !== -1 && fromIndex < toIndex;
    }

    export function startTimeInCampus(bus: SchoolBusRoutine, campus: Campus): Option<Date> {
        return findFirst(bus, it => it.campusId === campus.id)
            .chain(it => some(it.startTime));
    }
}
