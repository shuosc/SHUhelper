import 'mocha';
import {expect} from "chai";
import {TimeService} from "./time";
import createTimeFromHourMinutesString = TimeService.createTimeFromHourMinuteString;
import createTime = TimeService.createTime;
import toChineseString = TimeService.toChineseString;
import toHourMinuteString = TimeService.toHourMinuteString;
import timestampDifferenceToHourMinutesString = TimeService.timestampDifferenceToHourMinutesString;
import timeDistance = TimeService.timeDistance;
import timestampDifferenceToHourMinutesChinese = TimeService.timestampDifferenceToHourMinutesChinese;


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
        expect(TimeService.timestampDifferenceToMinutes(TimeService.timeDistance(time1, time2))).equals(1);
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
    it('能从形如 hh:mm:ss 格式的字符串中构造出时间', async () => {
        expect(createTimeFromHourMinutesString("00:00").value.getTime())
            .equals(createTime(0, 0).getTime());
        expect(createTimeFromHourMinutesString("7:15:30").value.getTime())
            .equals(createTime(7, 15, 30).getTime());
        expect(createTimeFromHourMinutesString('错误:错误').isNull).true;
    });
    it('能从将时间格式化为hh点mm分ss秒 的格式', async () => {
        expect(toChineseString(createTime(5, 20)))
            .equals("5点20分0秒");
    });
    it('能从将时间格式化为hh:mm的格式', async () => {
        expect(toHourMinuteString(createTime(5, 20)))
            .equals("05:20");
    });
    it('能将单位为毫秒的时间差格式化为 hh:mm 的格式', async () => {
        const timestampDifference = timeDistance(createTime(0, 20), createTime(0, 30));
        expect(timestampDifferenceToHourMinutesString(timestampDifference))
            .equals("0:10");
        const timestampDifference2 = timeDistance(createTime(0, 20), createTime(1, 30));
        expect(timestampDifferenceToHourMinutesString(timestampDifference2))
            .equals("1:10");
    });
    it('将单位为毫秒的时间差格式化为hh小时mm分钟的格式', async () => {
        const timestampDifference = timeDistance(createTime(0, 20), createTime(0, 30));
        expect(timestampDifferenceToHourMinutesChinese(timestampDifference))
            .equals("10分钟");
        const timestampDifference2 = timeDistance(createTime(0, 20), createTime(1, 30));
        expect(timestampDifferenceToHourMinutesChinese(timestampDifference2))
            .equals("1小时10分钟");
    });
});