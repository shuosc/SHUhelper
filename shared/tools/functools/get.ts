import {just, Maybe} from "./maybe";

export function get<K, V>(map: Map<K, V>, key: K): Maybe<V> {
    return just(map.get(key));
}