import 'mocha';
import {expect} from 'chai';
import {DateRangeService} from "./dateRange";

describe('dateRange测试', async () => {
    it('能判断某一天是否是一个dateRange内', async () => {
        const dateRange = {
            begin: new Date(2019, 0, 1),
            end: new Date(2019, 11, 31)
        };
        expect(DateRangeService.isDateIn(dateRange, new Date(2019, 1, 1)));
    });
});