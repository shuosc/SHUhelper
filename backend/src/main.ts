import * as Koa from 'koa';
import * as Router from 'koa-router';
import * as mongoose from 'mongoose';
import * as Redis from 'ioredis';
import * as KoaBodyParser from 'koa-bodyparser';
import {login} from './service/login/login';
import {fetchCoursePage, parseCoursePage} from './service/crawl/courseTable/courseTable';
import {serializeCourse} from "./model/course";

const redis = new Redis();
const app = new Koa();
const router = new Router();
mongoose.connect('mongodb://localhost:4004/');

app.use(KoaBodyParser());

router.post('/api/courses', async (ctx: Router.IRouterContext) => {
    const username = ctx.request.body['username'];
    const password = ctx.request.body['password'];
    const cookies = await login('http://xk.autoisp.shu.edu.cn', username, password);
    const coursePage = await fetchCoursePage(username, cookies);
    ctx.res.setHeader('Content-Type', 'application/json');
    ctx.body = (await parseCoursePage(coursePage)).map(serializeCourse);
}).get('/*', async (ctx: Router.IRouterContext) => {
    ctx.body = 'It works!';
});

app.use(router.routes());

app.listen(3001);

console.log('Server running on port 3001');

