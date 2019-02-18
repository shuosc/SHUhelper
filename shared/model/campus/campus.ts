import {Maybe} from "../../tools/functools/maybe";
import {find} from "../../tools/functools/array/array";

export interface Campus {
    id: number,
    name: string,
}

export namespace CampusRepository {
    export const all = [
        {id: 0, name: '本部'},
        {id: 1, name: '延长'},
        {id: 2, name: '嘉定'}
    ];

    export function getById(id: number): Maybe<Campus> {
        return find(all, (it) => it.id === id);
    }

    export function getByName(name: string): Maybe<Campus> {
        return find(all, (it) => it.name === name);
    }
}