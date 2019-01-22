import {Maybe} from "./maybe";

export function get<K, V>(map: Map<K, V>, key: K): Maybe<V> {
    return new Maybe<V>(map.get(key));
}