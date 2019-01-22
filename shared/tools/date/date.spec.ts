import 'mocha';
import {expect} from 'chai';
import {DateService, DAY_NUMBER_TO_CHINESE, mergeDateTime} from "./date";
import {TimeService} from "../time/time";


describe('Date 测试', async () => {
    it('能使用人类的格式创建一个日期对象', async () => {
        const date = DateService.createDate(2019, 1, 1);
        expect(date.getFullYear()).equals(2019);
        expect(date.getMonth()).equals(0);
        expect(date.getDate()).equals(1);
        expect(DAY_NUMBER_TO_CHINESE[date.getDay()]).equals('二');
    });
    it('能合并日期和时间', async () => {
        const date = DateService.createDate(2019, 1, 1);
        const time = TimeService.createTime(10, 10);
        const dateTime = mergeDateTime(date, time);
        expect(dateTime.getFullYear()).equals(2019);
        expect(dateTime.getMonth()).equals(0);
        expect(dateTime.getDate()).equals(1);
        expect(DAY_NUMBER_TO_CHINESE[dateTime.getDay()]).equals('二');
        expect(dateTime.getHours()).equals(10);
        expect(dateTime.getMinutes()).equals(10);
        expect(dateTime.getSeconds()).equals(0);
    });
    it('能判断两个日期是否是同一天', async () => {
        const date1 = mergeDateTime(DateService.createDate(2019, 1, 1), TimeService.createTime(10, 10));
        const date2 = mergeDateTime(DateService.createDate(2019, 1, 1), TimeService.createTime(20, 20));
        expect(DateService.isSameDate(date1, date2)).true;
        const date3 = mergeDateTime(DateService.createDate(2019, 1, 2), TimeService.createTime(20, 20));
        expect(DateService.isSameDate(date2, date3)).false;
    });
    it('能求下一周的这一天', async () => {
        (function testCase1() {
            const date = DateService.createDate(2019, 1, 1);
            const nextWeekDate = DateService.toNextWeek(date);
            expect(nextWeekDate.getFullYear()).equals(2019);
            expect(nextWeekDate.getMonth()).equals(0);
            expect(nextWeekDate.getDate()).equals(8);
        })();
        (function testCase2() {
            const date = DateService.createDate(2019, 1, 31);
            const nextWeekDate = DateService.toNextWeek(date);
            expect(nextWeekDate.getFullYear()).equals(2019);
            expect(nextWeekDate.getMonth()).equals(1);
            expect(nextWeekDate.getDate()).equals(7);
        })();
        (function testCase3() {
            const date = DateService.createDate(2018, 12, 25);
            const nextWeekDate = DateService.toNextWeek(date);
            expect(nextWeekDate.getFullYear()).equals(2019);
            expect(nextWeekDate.getMonth()).equals(0);
            expect(nextWeekDate.getDate()).equals(1);
        })();
    });
    it('能求上一周的这一天', async () => {
        (function testCase1() {
            const date = DateService.createDate(2019, 1, 8);
            const nextWeekDate = DateService.toLastWeek(date);
            expect(nextWeekDate.getFullYear()).equals(2019);
            expect(nextWeekDate.getMonth()).equals(0);
            expect(nextWeekDate.getDate()).equals(1);
        })();
        (function testCase2() {
            const date = DateService.createDate(2019, 2, 7);
            const nextWeekDate = DateService.toLastWeek(date);
            expect(nextWeekDate.getFullYear()).equals(2019);
            expect(nextWeekDate.getMonth()).equals(0);
            expect(nextWeekDate.getDate()).equals(31);
        })();
        (function testCase3() {
            const date = DateService.createDate(2019, 1, 1);
            const nextWeekDate = DateService.toLastWeek(date);
            expect(nextWeekDate.getFullYear()).equals(2018);
            expect(nextWeekDate.getMonth()).equals(11);
            expect(nextWeekDate.getDate()).equals(25);
        })();
    });
});