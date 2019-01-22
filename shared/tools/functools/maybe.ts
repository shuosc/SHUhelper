import {clone} from "../clone";

/**
 * 代表可选值(T | null)
 * @see Haskell 的 Maybe、Scala的Optional
 * @note 这是一个 Monad
 */
export class Maybe<T> {
    readonly value: T | null;

    constructor(value: T | null | undefined | Maybe<T>) {
        // I hate the fact that we have two values which means "no value"
        if (value === undefined) {
            this.value = null;
        } else if (value instanceof Maybe) {
            this.value = clone(value.value);
        } else {
            this.value = value;
        }
    }

    // make it a Functor!
    public map<U>(func: (value: T) => U): Maybe<U> {
        if (this.value === null) {
            return new Maybe<U>(null);
        }
        return new Maybe(func(this.value));
    }

    // make it an Applicative!
    public apply<U>(func: Maybe<(value: T) => U>): Maybe<U> {
        if (func.value === null) {
            return new Maybe<U>(null);
        }
        return this.map(func.value);
    }

    // make it a Monad!
    public flatMap<U>(func: (value: T) => Maybe<U>): Maybe<U> {
        if (this.value === null) {
            return new Maybe<U>(null);
        }
        return func(this.value);
    }
}
