import 'mocha';
import {expect} from 'chai';
import {DateRangeService} from "./dateRange";
import {createDate} from "../../tools/date";

describe('dateRange测试', async () => {
    it('能判断某一天是否是一个dateRange内', async () => {
        const dateRange = {
            begin: createDate(2019, 1, 21),
            end: createDate(2019, 2, 25)
        };
        expect(DateRangeService.isDateIn(dateRange, createDate(2019, 1, 21)));
        expect(DateRangeService.isDateIn(dateRange, createDate(2019, 2, 1)));
        expect(DateRangeService.isDateIn(dateRange, createDate(2019, 2, 24)));
    });
});