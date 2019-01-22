import 'mocha';
import {expect} from 'chai';
import {DateRangeService} from "../../dateRange/dateRange";

describe('dateRange测试', async () => {
    it('能判断某一天是否是一个Holiday内', async () => {
        const holiday = {
            name: '某次寒假',
            begin: new Date(2019, 0, 1),
            end: new Date(2019, 1, 1)
        };
        expect(DateRangeService.isDateIn(holiday, new Date(2019, 0, 10))).true;
        expect(DateRangeService.isDateIn(holiday, new Date(2019, 10, 10))).false;
    });
});