import 'mocha';
import {Semester, SemesterService} from "./semester";
import {expect} from 'chai';
import {DateService} from "../../tools/dateTime/date/date";
import createDate = DateService.createDate;

const semester: Semester = {
    _id: null,
    name: "测试",
    begin: createDate(2018, 11, 26),
    end: createDate(2019, 3, 24),
    holidays: [{
        name: '寒假',
        begin: createDate(2019, 1, 21),
        end: createDate(2019, 2, 25)
    }, {
        name: '元旦假',
        begin: createDate(2018, 12, 30),
        end: createDate(2019, 1, 1),
        shifts: [
            {
                from: createDate(2019, 1, 1),
                to: createDate(2018, 12, 30)
            }
        ]
    }]
};

describe('semester测试', async () => {
    it('能判断某天是否是假期', async () => {
        expect(SemesterService.isHoliday(semester, createDate(2018, 11, 26))).false;
        expect(SemesterService.isHoliday(semester, createDate(2018, 12, 2))).false;
        expect(SemesterService.isHoliday(semester, createDate(2019, 1, 21))).true;
        expect(SemesterService.isHoliday(semester, createDate(2019, 2, 24))).true;
        expect(SemesterService.isHoliday(semester, createDate(2019, 1, 1))).true;
        expect(SemesterService.isHoliday(semester, createDate(2018, 12, 30))).false;
    });
    it('能获取到某一天上哪天的课', async () => {
        expect(SemesterService.getSchoolDay(semester, createDate(2018, 12, 30))).equals(2);
        expect(SemesterService.getSchoolDay(semester, createDate(2019, 1, 1))).equals(SemesterService.HOLIDAY);
    });
    it('能判断某一天是这个学期的第几周', async () => {
        expect(SemesterService.getWeekIndex(semester, createDate(2018, 11, 26))).equals(1);
        expect(SemesterService.getWeekIndex(semester, createDate(2018, 12, 2))).equals(1);
        expect(SemesterService.getWeekIndex(semester, createDate(2018, 12, 2))).equals(1);
        expect(SemesterService.getWeekIndex(semester, createDate(2019, 1, 14))).equals(8);
        expect(SemesterService.getWeekIndex(semester, createDate(2019, 1, 20))).equals(8);
        expect(SemesterService.getWeekIndex(semester, createDate(2019, 1, 21))).equals(0);
        expect(SemesterService.getWeekIndex(semester, createDate(2019, 2, 24))).equals(0);
        expect(SemesterService.getWeekIndex(semester, createDate(2019, 2, 25))).equals(9);
        expect(SemesterService.getWeekIndex(semester, createDate(2019, 3, 10))).equals(10);
        expect(SemesterService.getWeekIndex(semester, createDate(2018, 12, 30))).equals(
            SemesterService.getWeekIndex(semester, createDate(2019, 1, 2)));
    });
    it('能获取总的工作日数量', async () => {
        expect(SemesterService.getTotalWorkingDayCount(semester)).equals(58);
    });
});