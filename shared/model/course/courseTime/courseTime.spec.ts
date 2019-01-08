import 'mocha';
import {expect} from 'chai';
import {CourseTimeService} from "./courseTime";

describe('courseTime测试', async () => {
    it('能用字符串构造', async () => {
        const courseTime = CourseTimeService.fromString('一1-2');
        expect(courseTime).not.null;
        expect(courseTime.day).equals(1);
        expect(courseTime.beginSector).equals(1);
        expect(courseTime.endSector).equals(2);
    })
});