import * as Koa from 'koa';
import * as Router from 'koa-router';
import * as KoaBodyParser from 'koa-bodyparser';
import * as KoaLogger from 'koa-logger';
import * as jwt from 'jsonwebtoken';
import {initDB} from "./infrastructure/mongodb";
import {simulateLogin} from "./service/simulateLogin/simulateLogin";
import {Student, StudentRepository} from "./model/student";
import {authMiddleware} from "./middleware/auth";
import {initSemesters} from "./model/semester/semester";

const app = new Koa();
const router = new Router();

app.use(KoaBodyParser());
app.use(KoaLogger());
app.use(authMiddleware);

router
    .post('/auth/login', async (ctx: Router.IRouterContext) => {
        const username = ctx.request.body['username'];
        const password = ctx.request.body['password'];
        let theStudent = await StudentRepository.getById(username);
        if (theStudent === null) {
            const cookies = await simulateLogin('http://xk.autoisp.shu.edu.cn', username, password);
            theStudent = new Student(username);
            theStudent.xkCookie = cookies[0];
            await StudentRepository.save(theStudent);
        }
        let token = jwt.sign({user: username}, process.env['JWT_SECRET'], {expiresIn: 60 * 60 * 24 * 7});
        ctx.body = {
            token: token,
            name: await theStudent.getName()
        }
    })
    .get('/api/courses', async (ctx: Router.IRouterContext) => {
        const courses = await ctx.request.user.getCourses();
        ctx.body = courses.map(it => it.serialize());
    })
    .get('/*', async (ctx: Router.IRouterContext) => {
        ctx.body = 'It works!';
    });

app.use(router.routes());

(async () => {
    await initDB();
    await initSemesters();
    app.listen(3001);
    console.log('Server running on port 3001');
})();
