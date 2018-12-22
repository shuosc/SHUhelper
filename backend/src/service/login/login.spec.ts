import {login} from './login';
import 'mocha';
import * as Request from 'request-promise-native';
import {expect} from 'chai';

describe('模拟登录测试', () => {
    it('登录并拿到Cookie', async () => {
        const cookies = await login('http://xk.autoisp.shu.edu.cn', process.env.STUDENT_ID, process.env.PASSWORD);
        expect(cookies[0].cookieString().indexOf('ASP.NET_SessionId')).not.equal(-1);
    });
    it('拿到的Cookie可以用于访问课程列表', async () => {
        const cookie = await login('http://xk.autoisp.shu.edu.cn', process.env.STUDENT_ID, process.env.PASSWORD);
        let cookiejar = Request.jar();
        cookiejar.setCookie(cookie[0], 'http://xk.autoisp.shu.edu.cn');
        let page = await Request.post('http://xk.autoisp.shu.edu.cn/StudentQuery/CtrlViewQueryCourseTable', {
            jar: cookiejar,
            form: {
                studentNo: process.env.STUDENT_ID
            }
        });
        expect(page.indexOf('学号：&nbsp;&nbsp;&nbsp;' + process.env.STUDENT_ID)).not.equal(-1);
    });
    it('成绩页面可以用同样的方式来登录', async () => {
        const cookie = await login('http://cj.shu.edu.cn', process.env.STUDENT_ID, process.env.PASSWORD);
        let cookiejar = Request.jar();
        cookiejar.setCookie(cookie[0], 'http://cj.shu.edu.cn');
        let page = await Request.get('http://cj.shu.edu.cn/Home/StudentIndex');
        expect(page.indexOf('欢迎')).not.equal(-1);
    });
});