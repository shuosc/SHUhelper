import 'mocha';
import {expect} from 'chai';
import {DateRangeService} from "./dateRange";
import {DateService} from "../../tools/dateTime/date/date";
import createDate = DateService.createDate;

describe('dateRange测试', async () => {
    it('能判断某一天是否是一个dateRange内', async () => {
        const dateRange = {
            begin: createDate(2019, 1, 21),
            end: createDate(2019, 2, 25)
        };
        expect(DateRangeService.isDateIn(dateRange, createDate(2019, 1, 21))).true;
        expect(DateRangeService.isDateIn(dateRange, createDate(2019, 2, 1))).true;
        expect(DateRangeService.isDateIn(dateRange, createDate(2019, 2, 24))).true;
        expect(DateRangeService.isDateIn(dateRange, createDate(2019, 2, 25))).false;
    });
    it('能求 dateRanges 之中，开始在 date 之后的中的最先的一个', async () => {
        const dateRanges = [{
            begin: createDate(2019, 1, 1),
            end: createDate(2019, 2, 1),
        }, {
            begin: createDate(2019, 4, 1),
            end: createDate(2019, 5, 1),
        }, {
            begin: createDate(2019, 2, 1),
            end: createDate(2019, 3, 1),
        }];
        expect(DateRangeService.nextFromDate(dateRanges, createDate(2019, 3, 1)).value.begin.getMonth()).equals(3);
        expect(DateRangeService.nextFromDate(dateRanges, createDate(2019, 6, 1)).value).is.null;
    });
    it('能返回 date 距离 dateRange 的天数', async () => {
        const dateRange = {
            begin: createDate(2019, 2, 1),
            end: createDate(2019, 3, 1),
        };
        const date = createDate(2019, 1, 30);
        const date2 = createDate(2019, 2, 2);
        const date3 = createDate(2019, 3, 2);
        expect(DateRangeService.daysTo(date, dateRange)).equals(2);
        expect(DateRangeService.daysTo(date2, dateRange)).equals(0);
        expect(DateRangeService.daysTo(date3, dateRange)).equals(1);
    });
});