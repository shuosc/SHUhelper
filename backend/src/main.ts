import * as Koa from 'koa';
import * as Router from 'koa-router';
import * as KoaBodyParser from 'koa-bodyparser';
import * as KoaLogger from 'koa-logger';
import * as jwt from 'jsonwebtoken';
import {authMiddleware} from "./middleware/auth";
import {initDB} from "./infrastructure/mongo";
import {initSemesters} from "./model/semester/semester";
import {StudentRepository, StudentService} from "./model/student/student";
import {CourseRepository} from "./model/course/course";

const app = new Koa();
const router = new Router();

app.use(KoaBodyParser());
app.use(KoaLogger());
app.use(authMiddleware);

router
    .post('/auth/login', async (context) => {
        const username = context.request.body['username'];
        const password = context.request.body['password'];
        const theStudent = await StudentService.login(username, password);
        if (theStudent === null) {
            context.status = 403;
            return;
        }
        await StudentRepository.save(theStudent);
        let token = jwt.sign({user: username}, process.env['JWT_SECRET'], {expiresIn: 60 * 60 * 24 * 7});
        context.body = {
            token: token,
            name: theStudent.name
        }
    })
    .get('/api/courses', async (context) => {
        if (context.request.user === null) {
            context.status = 403;
        } else {
            context.body = await Promise.all(context.request.user.courseIds.map(id => CourseRepository.getById(id)));
        }
    })
    .get('/*', async (context) => {
        context.body = 'It works!';
    });

app.use(router.routes());

(async () => {
    await initDB();
    await initSemesters();
    app.listen(3001);
    console.log('Server running on port 3001');
})();
