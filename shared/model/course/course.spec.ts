import 'mocha';
import {expect} from 'chai';
import {Semester} from "../semester/semester";
import {DateService} from "../../tools/dateTime/date/date";
import {Course, CourseService} from "./course";

const semester: Semester = {
    _id: "testId",
    name: "a test semester",
    holidays: [],
    begin: DateService.createDate(2018, 1, 1),
    end: DateService.createDate(2019, 1, 1)
};

const courses: Array<Course> = [
    {
        id: null,
        name: "测试课程1",
        teacherId: null,
        semesterId: "testId",
        classes: [{
            courseId: null,
            day: 1,
            beginSector: 1,
            endSector: 3,
            weeks: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        }],
        place: ""
    }, {
        id: null,
        name: "测试课程2",
        teacherId: null,
        semesterId: "testId2",
        classes: [{
            courseId: null,
            day: 1,
            beginSector: 1,
            endSector: 3,
            weeks: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        }],
        place: ""
    }
];

describe('Course 测试', async () => {
    it('能判断某节课是否是某个学期内的课', async () => {
        expect(CourseService.isInSemester(courses[0], semester)).true;
        expect(CourseService.isInSemester(courses[1], semester)).false;
    });
    it('能判断某个课程是否在某天有课', async () => {
        expect(CourseService.hasClassOnDate(courses[0], semester, DateService.createDate(2018, 1, 1))).true;
        expect(CourseService.hasClassOnDate(courses[0], semester, DateService.createDate(2018, 1, 2))).false;
        expect(CourseService.hasClassOnDate(courses[0], semester, DateService.createDate(2018, 1, 8))).true;
    });
    it('能从课程列表中解出所有的课', async () => {
        expect(CourseService.extractClasses(courses).length).equals(2);
    });
});
