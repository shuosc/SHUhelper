import 'mocha';
import {expect} from "chai";
import {TimeService} from "./time";


describe('Time 测试', async () => {
    it('能创建一个时间对象', async () => {
        const time = TimeService.createTime(10, 10);
        expect(time.getHours()).equals(10);
        expect(time.getMinutes()).equals(10);
        expect(time.getSeconds()).equals(0);
    });
});