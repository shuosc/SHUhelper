import 'mocha';
import * as Request from 'request-promise-native';
import {expect} from 'chai';

describe('api可用', async () => {
    it('能登录', async () => {
        await new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve();
            }, 500)
        });
        let response = await Request.post({
            uri: 'http://localhost:3001/auth/login',
            body: {
                username: process.env.STUDENT_ID,
                password: process.env.PASSWORD
            },
            json: true
        });
        expect(response.token).not.equals(undefined);
    });
    it('能拿到课程', async () => {
        let response = await Request.post({
            uri: 'http://localhost:3001/auth/login',
            body: {
                username: process.env.STUDENT_ID,
                password: process.env.PASSWORD
            },
            json: true
        });
        response = await Request.get({
            uri: 'http://localhost:3001/api/courses',
            headers: {
                Authorization: 'Bearer ' + response.token
            }
        });
        expect(response.length).not.equals(0);
        expect(response[0]).not.equals(null);
    });
});