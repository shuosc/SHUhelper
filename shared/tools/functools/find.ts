import {Maybe} from "./maybe";

export function find<T>(array: Array<T>, pred: (value: T) => boolean): Maybe<T> {
    return new Maybe(array.find(pred));
}

export function findIndex<T>(array: Array<T>, pred: (value: T) => boolean): Maybe<number> {
    for (let i = 0; i < array.length; ++i) {
        if (pred(array[i])) {
            return new Maybe(i);
        }
    }
    return new Maybe<number>(null);
}