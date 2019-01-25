import * as Koa from 'koa';
import * as jwt from 'jsonwebtoken';
import {Student, StudentRepository} from "../model/student/student";
import {just, Maybe} from "../../../shared/tools/functools/maybe";

declare module "koa" {
    interface Request {
        student: Maybe<Student>;
    }
}

/**
 * 鉴权中间件
 */
export async function authMiddleware(ctx: Koa.Context, next) {
    try {
        let token = ctx.request.header['authorization'].slice('Bearer '.length);
        let decoded = jwt.decode(token);
        ctx.request.student = just(await StudentRepository.getById(decoded['student']));
    } catch (e) {
        if (e instanceof TypeError) {
            ctx.request.student = just(null);
        }
    }
    await next();
}