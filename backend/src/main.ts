import * as Koa from 'koa';
import * as Router from 'koa-router';
import * as mongoose from 'mongoose';
import { Test } from './model/test';
import * as Redis from 'ioredis';

const redis = new Redis();
const app = new Koa();
const router = new Router();
mongoose.connect('mongodb://localhost:4004/');

router.get('/*', async (ctx: Router.IRouterContext) => {
  // this is only a tempory test to make sure we really connected to our db
  // will be removed soon
  let t = await Test.create({ name: ctx.URL });
  let last = await redis.get('last-id');
  redis.set('last-id', t.id);
  ctx.res.setHeader('Content-Type', 'application/json');
  ctx.body = {
    last: last,
    id: t.id,
    count: await Test.find({}).count()
  };
});

app.use(router.routes());

app.listen(3001);

console.log('Server running on port 3001');