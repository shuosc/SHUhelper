import {Option} from "~/node_modules/fp-ts/lib/Option";
import {findFirst} from "~/node_modules/fp-ts/lib/Array";
import {Campus} from "../../shared/model/campus/campus";

export namespace CampusRepository {
    export const all = [
        {id: 0, name: '本部'},
        {id: 1, name: '延长'},
        {id: 2, name: '嘉定'}
    ];

    export function getById(id: number): Option<Campus> {
        return findFirst(all, (it) => it.id === id);
    }

    export function getByName(name: string): Option<Campus> {
        return findFirst(all, (it) => it.name === name);
    }
}