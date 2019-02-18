import * as Redis from 'ioredis';

export const redis = new Redis(process.env['REDIS_ADDRESS']);

export namespace RedisService {
    export async function cache(collectionName: string, object: { id?: any, _id?: any }) {
        let data = JSON.stringify(object);
        if (object.id !== undefined) {
            await redis.set(`${collectionName}_${object.id}`, data);
        } else if (object._id !== undefined) {
            await redis.set(`${collectionName}_${object._id}`, data);
        } else {
            throw Error("Cannot cache an object without an id!");
        }
    }
}