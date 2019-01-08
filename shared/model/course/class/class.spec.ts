import 'mocha';
import {expect} from 'chai';
import {Class, ClassService} from "./class";
import {Semester} from "../../semester/semester";
import {createDate} from "../../../tools/date";

describe('Class 测试', async () => {
    it('能用字符串构造', async () => {
        const courseTime = ClassService.fromString('一1-2');
        expect(courseTime).not.null;
        expect(courseTime.day).equals(1);
        expect(courseTime.beginSector).equals(1);
        expect(courseTime.endSector).equals(2);
    });
    it('能判断某节课是否在这一天', async () => {
        const semester: Semester = {
            _id: null,
            name: '',
            holidays: [{
                name: '寒假',
                begin: createDate(2019, 1, 21),
                end: createDate(2019, 2, 25)
            }],
            begin: createDate(2018, 11, 26),
            end: createDate(2019, 3, 24)
        };
        const theClass: Class = {
            day: 1,
            beginSector: 1,
            endSector: 2,
            weeks: [1, 3, 5, 7, 9]
        };
        expect(ClassService.isOnDate(theClass, semester, createDate(2018, 11, 26))).true;
        expect(ClassService.isOnDate(theClass, semester, createDate(2018, 12, 3))).false;
        expect(ClassService.isOnDate(theClass, semester, createDate(2018, 11, 27))).false;
        expect(ClassService.isOnDate(theClass, semester, createDate(2019, 1, 21))).false;
        expect(ClassService.isOnDate(theClass, semester, createDate(2019, 2, 25))).true;
    });
});