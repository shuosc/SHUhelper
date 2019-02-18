import {just, Maybe} from "../maybe";

export function findIndex<T>(array: Array<T>, pred: (value: T) => boolean): Maybe<number> {
    for (let i = 0; i < array.length; ++i) {
        if (pred(array[i])) {
            return new Maybe(i);
        }
    }
    return new Maybe<number>(null);
}

export function find<T>(array: Array<T>, pred: (value: T) => boolean): Maybe<T> {
    return new Maybe(array.find(pred));
}

export function findIndexBefore<T>(array: Array<T>, pred: (value: T) => boolean): Maybe<number> {
    return findIndex(array, pred).flatMap(it => it > 0 ? just(it - 1) : just<number>(null));
}

export function findBefore<T>(array: Array<T>, pred: (value: T) => boolean): Maybe<T> {
    return findIndexBefore(array, pred).map(it => array[it]);
}
