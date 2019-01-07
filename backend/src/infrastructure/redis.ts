import * as Redis from 'ioredis';

export const redis = new Redis(process.env['REDIS_ADDRESS']);