import * as Koa from 'koa';
import * as Router from 'koa-router';
import * as KoaBodyParser from 'koa-bodyparser';
import * as KoaLogger from 'koa-logger';
import {initDB} from "./infrastructure/mongo";
import {SemesterRepository} from "./model/semester/semester";
import {adminAuthMiddleware, authMiddleware} from "./middleware/auth";
import {ObjectID} from "bson";
import {StudentRepository, StudentService} from "./model/student/student";
import * as jwt from 'jsonwebtoken';
import {CourseRepository} from "./model/course/course";
import {normalizeDateTimeInObject} from "../tools/dateTime";

const app = new Koa();
const router = new Router();

app.use(KoaBodyParser());
app.use(KoaLogger());
app.use(authMiddleware);
app.use(adminAuthMiddleware);

async function saveSemesterInContext(id, context) {
    await SemesterRepository.save({
        _id: new ObjectID(id),
        ...normalizeDateTimeInObject({
            start: context.request.body.start,
            end: context.request.body.end,
            holidays: context.request.body.holidays,
            name: context.request.body.name,
            courseSelectionPort8080: context.request.body.courseSelectionPort8080
        })
    });
}

router
    .post('/auth/login', async (context) => {
        const username = context.request.body['username'];
        const password = context.request.body['password'];
        const theStudent = await StudentService.login(username, password);
        if (theStudent.isNone()) {
            context.status = 403;
            return;
        }
        await theStudent.map(StudentRepository.save).toNullable();
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
    .get('/api/course/:id', async (context) => {
        context.body = (await CourseRepository.getById(context.params.id)).toNullable();
    })
    .get('/api/student', async (context) => {
        if (context.request.student.isNone()) {
            context.status = 403;
        } else {
            context.body = context.request.student.map(student => {
                return {
                    id: student.id,
                    name: student.name,
                    courseIds: student.courseIds
                }
            }).toNullable();
        }
    })
    .get('/api/semesters', async (context) => {
        context.body = (await SemesterRepository.all());
    })
    .get('/api/semester/current', async (context) => {
        context.body = (await SemesterRepository.current()).getOrElseL(() => {
            context.state = 404;
            return null;
        });
    })
    .get('/api/semester/:id', async (context) => {
        context.body = (await SemesterRepository.getById(context.params.id)).getOrElseL(() => {
            context.state = 404;
            return null;
        });
    })
    .get('/api/semester', async (context) => {
        const dateTime = context.query.time === "current" ? new Date() : new Date(context.query.time);
        context.body = (await SemesterRepository.getByDate(dateTime)).getOrElseL(() => {
            context.state = 404;
            return null;
        });
    })
    .post('/api/semester/', async (context) => {
        if (context.request.admin) {
            const id = new ObjectID();
            await saveSemesterInContext(id, context);
            context.body = {
                success: true,
                result: (await SemesterRepository.getById(id)).toNullable()
            }
        } else {
            context.status = 403;
        }
    })
    .put('/api/semester/:id', async (context) => {
        if (context.request.admin) {
            const id = new ObjectID(context.params.id);
            await saveSemesterInContext(id, context);
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
    .get('/', async (context) => {
        context.body = 'It works!';
    })
    .get('/*', async (context) => {
        context.status = 404;
    });

app.use(router.routes());

(async () => {
    await initDB();
    app.listen(3001);
    console.log('Server running on port 3001');
})();
