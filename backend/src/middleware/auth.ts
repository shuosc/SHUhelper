import * as Koa from 'koa';
import * as jwt from 'jsonwebtoken';
import {Student, StudentRepository} from "../model/student";

declare module "koa" {
    interface Request {
        user: Student;
    }
}

export async function authMiddleware(ctx: Koa.Context, next) {
    try {
        let token = ctx.request.header['authorization'].slice(7);
        let decoded = jwt.decode(token);
        ctx.request.user = await StudentRepository.getById(decoded['user']);
    } catch (e) {
        if (e instanceof TypeError) {
            ctx.request.user = null;
        }
    }
    await next();
}