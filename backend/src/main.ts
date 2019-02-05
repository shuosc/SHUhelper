import * as Koa from 'koa';
import * as Router from 'koa-router';
import * as KoaBodyParser from 'koa-bodyparser';
import * as KoaLogger from 'koa-logger';
import * as jwt from 'jsonwebtoken';
import {adminAuthMiddleware, authMiddleware} from "./middleware/auth";
import {initDB} from "./infrastructure/mongo";
import {initSemesters, SemesterRepository} from "./model/semester/semester";
import {CourseRepository} from "./model/course/course";
import {StudentRepository, StudentService} from "./model/student/student";
import {ObjectID} from "bson";
import {DateTimeService} from "../../shared/tools/dateTime/dateTime";

const app = new Koa();
const router = new Router();

app.use(KoaBodyParser());
app.use(KoaLogger());
app.use(authMiddleware);
app.use(adminAuthMiddleware);

router
    .post('/auth/login', async (context) => {
        const username = context.request.body['username'];
        const password = context.request.body['password'];
        const theStudent = await StudentService.login(username, password);
        if (theStudent === null) {
            context.status = 403;
            return;
        }
        await theStudent.map(StudentRepository.save).value;
        let token = jwt.sign({student: username}, process.env['JWT_SECRET'], {expiresIn: 60 * 60 * 24 * 7});
        context.body = {
            token: token
        }
    })
    .post('/auth/check-token', async (context) => {
        context.body = {
            success: context.request.body['token'] === process.env['ADMIN_TOKEN']
        }
    })
    .get('/api/student', async (context) => {
        if (context.request.student === null) {
            context.status = 403;
        } else {
            context.body = context.request.student.map(student => {
                return {
                    id: student.id,
                    name: student.name,
                    courseIds: student.courseIds
                }
            }).value;
        }
    })
    .get('/api/course/:id', async (context) => {
        context.body = (await CourseRepository.getById(context.params.id)).value;
    })
    .get('/api/semesters', async (context) => {
        context.body = (await SemesterRepository.all());
    })
    .get('/api/semester/current', async (context) => {
        context.body = (await SemesterRepository.current()).value;
    })
    .get('/api/semester/:id', async (context) => {
        context.body = (await SemesterRepository.getById(context.params.id)).value;
    })
    .post('/api/semester/', async (context) => {
        if (context.request.admin) {
            const id = new ObjectID();
            await SemesterRepository.save({
                _id: id,
                ...DateTimeService.normalizeDateInObject({
                    begin: context.request.body.begin,
                    end: context.request.body.end,
                    holidays: context.request.body.holidays,
                    name: context.request.body.name
                })
            });
            context.body = {
                success: true,
                result: (await SemesterRepository.getById(id)).value
            }
        } else {
            context.status = 403;
        }
    })
    .put('/api/semester/:id', async (context) => {
        if (context.request.admin) {
            await SemesterRepository.save({
                _id: new ObjectID(context.params.id),
                ...DateTimeService.normalizeDateInObject({
                    begin: context.request.body.begin,
                    end: context.request.body.end,
                    holidays: context.request.body.holidays,
                    name: context.request.body.name
                })
            });
            context.body = {
                success: true
            }
        } else {
            context.status = 403;
        }
    })
    .delete('/api/semester/:id', async (context) => {
        if (context.request.admin) {
            await SemesterRepository.remove(new ObjectID(context.params.id));
            context.body = {
                success: true
            }
        } else {
            context.status = 403;
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
