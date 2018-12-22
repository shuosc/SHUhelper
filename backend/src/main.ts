import * as Koa from 'koa';
import * as Router from 'koa-router';
import * as mongoose from 'mongoose';
import * as KoaBodyParser from 'koa-bodyparser';
import * as jwt from 'jsonwebtoken';
import {login} from './service/login/login';
import {fetchCoursePage, parseCoursePage} from './service/crawl/courseTable/courseTable';
import {serializeCourse} from "./model/course";
import {authMiddleware} from "./service/auth/middleware";
import {redis} from "./infrastructure/redis";

const app = new Koa();
const router = new Router();
mongoose.connect('mongodb://localhost:4004/');

app.use(KoaBodyParser());
app.use(authMiddleware);
router
    .post('/auth/login', async (ctx: Router.IRouterContext) => {
        const username = ctx.request.body['username'];
        const password = ctx.request.body['password'];
        const cookies = await login('http://xk.autoisp.shu.edu.cn', username, password);
        await redis.set(username + '_xk_cookie', JSON.stringify(cookies[0].toJSON()));
        let token = jwt.sign({user: username}, process.env['JWT_SECRET'], {expiresIn: 60 * 60 * 24 * 7});
        ctx.body = {
            token: token
        }
    })
    .post('/api/courses', async (ctx: Router.IRouterContext) => {
        console.log(ctx.request.user);
        const coursePage = await fetchCoursePage(ctx.request.user.username, [ctx.request.user.xk_cookie]);
        ctx.res.setHeader('Content-Type', 'application/json');
        ctx.body = (await parseCoursePage(coursePage)).map(serializeCourse);
    }).get('/*', async (ctx: Router.IRouterContext) => {
    ctx.body = 'It works!';
});

app.use(router.routes());

app.listen(3001);

console.log('Server running on port 3001');

