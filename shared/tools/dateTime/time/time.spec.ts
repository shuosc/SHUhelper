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
    it('能计算两个时间点之间的时间差', async () => {
        const time1 = TimeService.createTime(0, 1, 0);
        const time2 = TimeService.createTime(0, 2, 0);
        expect(TimeService.timeDistance(time1, time2)).equals(1000 * 60);
        expect(TimeService.timestampDifferenceToSeconds(TimeService.timeDistance(time1, time2))).equals(60);
    });
    it('能比较两个时间点的早晚关系', async () => {
        const time1 = TimeService.createTime(0, 1, 0);
        const time2 = TimeService.createTime(0, 2, 0);
        expect(TimeService.earlierThan(time1, time2)).true;
        expect(TimeService.earlierThan(time2, time1)).false;
        expect(TimeService.laterThan(time1, time2)).false;
        expect(TimeService.laterThan(time2, time1)).true;
        expect(TimeService.earlierThan(time1, time1)).false;
        expect(TimeService.earlierThan(time2, time2)).false;
        expect(TimeService.laterThan(time1, time1)).true;
        expect(TimeService.laterThan(time2, time2)).true;
    });
});