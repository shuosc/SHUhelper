import {Cookie} from "tough-cookie";
import * as Koa from 'koa';
import * as jwt from 'jsonwebtoken';
import {redis} from "../../infrastructure/redis";

declare module "koa" {
    interface Request {
        user: {
            username: string,
            xk_cookie: Cookie
        };
    }
}

export async function authMiddleware(ctx: Koa.Context, next) {
    let token = ctx.request.header['authorization'].slice(7);
    let decoded = jwt.decode(token);
    ctx.request.user = {
        username: decoded['user'],
        xk_cookie: Cookie.fromJSON(JSON.parse(await redis.get(decoded['user'] + '_xk_cookie')))
    };
    await next();
}