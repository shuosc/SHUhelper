import 'mocha';
import {expect} from 'chai';
import {Class, ClassService} from "./class";
import {Semester} from "../../semester/semester";
import {DateService} from "../../../tools/dateTime/date/date";
import createDate = DateService.createDate;

describe('Class 测试', async () => {
    it('能用字符串构造', async () => {
        (function testCase1() {
            const courseTime = ClassService.fromString('一1-2', null).value;
            expect(courseTime).not.null;
            expect(courseTime.day).equals(1);
            expect(courseTime.beginSector).equals(1);
            expect(courseTime.endSector).equals(2);
            expect(courseTime.weeks).contains(1);
            expect(courseTime.weeks).contains(2);
            expect(courseTime.weeks).contains(3);
            expect(courseTime.weeks).contains(5);
            expect(courseTime.weeks).contains(8);
        })();
        (function testCase2() {
            const courseTime = ClassService.fromString('一1-2单', null).value;
            expect(courseTime).not.null;
            expect(courseTime.day).equals(1);
            expect(courseTime.beginSector).equals(1);
            expect(courseTime.endSector).equals(2);
            expect(courseTime.weeks).contains(1);
            expect(courseTime.weeks).contains(3);
            expect(courseTime.weeks).contains(9);
            expect(courseTime.weeks).not.contains(2);
            expect(courseTime.weeks).not.contains(4);
            expect(courseTime.weeks).not.contains(8);
        })();
        (function testCase3() {
            const courseTime = ClassService.fromString('一1-2双', null).value;
            expect(courseTime).not.null;
            expect(courseTime.day).equals(1);
            expect(courseTime.beginSector).equals(1);
            expect(courseTime.endSector).equals(2);
            expect(courseTime.weeks).not.contains(1);
            expect(courseTime.weeks).not.contains(3);
            expect(courseTime.weeks).not.contains(9);
            expect(courseTime.weeks).contains(2);
            expect(courseTime.weeks).contains(4);
            expect(courseTime.weeks).contains(8);
        })();
        (function testCase4() {
            const courseTime = ClassService.fromString('一1-2 (1,4,9周)', null).value;
            expect(courseTime).not.null;
            expect(courseTime.day).equals(1);
            expect(courseTime.beginSector).equals(1);
            expect(courseTime.endSector).equals(2);
            expect(courseTime.weeks).contains(1);
            expect(courseTime.weeks).contains(4);
            expect(courseTime.weeks).contains(9);
            expect(courseTime.weeks).not.contains(2);
            expect(courseTime.weeks).not.contains(5);
            expect(courseTime.weeks).not.contains(8);
        })();
        (function testCase5() {
            const courseTime = ClassService.fromString('一1-2 (4-10周)', null).value;
            expect(courseTime).not.null;
            expect(courseTime.day).equals(1);
            expect(courseTime.beginSector).equals(1);
            expect(courseTime.endSector).equals(2);
            expect(courseTime.weeks).not.contains(1);
            expect(courseTime.weeks).not.contains(2);
            expect(courseTime.weeks).contains(4);
            expect(courseTime.weeks).contains(5);
            expect(courseTime.weeks).contains(8);
        })();
    });
    it('能判断某节课是否在这一天', async () => {
        const semester: Semester = {
            _id: null,
            name: '',
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
            }],
            begin: createDate(2018, 11, 26),
            end: createDate(2019, 3, 24)
        };
        const theClass: Class = {
            courseId: null,
            day: 2,
            beginSector: 1,
            endSector: 2,
            weeks: [1, 3, 5, 6, 7, 9]
        };
        expect(ClassService.isOnDate(theClass, semester, createDate(2018, 11, 27))).true;
        expect(ClassService.isOnDate(theClass, semester, createDate(2018, 12, 4))).false;
        expect(ClassService.isOnDate(theClass, semester, createDate(2018, 11, 28))).false;
        expect(ClassService.isOnDate(theClass, semester, createDate(2019, 1, 22))).false;
        expect(ClassService.isOnDate(theClass, semester, createDate(2019, 2, 26))).true;
        expect(ClassService.isOnDate(theClass, semester, createDate(2018, 12, 30))).true;
    });
    it('能判断某个 sector 是否在上 某节课', async () => {
        const theClass: Class = {
            courseId: null,
            day: 2,
            beginSector: 1,
            endSector: 3,
            weeks: [1, 3, 5, 6, 7, 9]
        };
        expect(ClassService.isOnSector(theClass, 1)).true;
        expect(ClassService.isOnSector(theClass, 2)).true;
        expect(ClassService.isOnSector(theClass, 3)).true;
        expect(ClassService.isOnSector(theClass, 4)).false;
        expect(ClassService.isOnSector(theClass, 5)).false;
    });
});