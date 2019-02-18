import 'mocha';
import {expect} from 'chai';
import {SchoolBusRepository, SchoolBusRoutine, SchoolBusRoutineType, SchoolBusService} from "./schoolBus";
import {CampusRepository} from "../campus/campus";
import {Semester} from "../semester/semester";
import {DateService} from "../../tools/dateTime/date/date";
import {DateTimeService} from "../../tools/dateTime/dateTime";
import {TimeService} from "../../tools/dateTime/time/time";
import createDate = DateService.createDate;
import mergeDateTime = DateTimeService.mergeDateTime;
import createTime = TimeService.createTime;

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
describe('schoolBus测试', async () => {
    const baoshanCampus = CampusRepository.getByName("本部").value;
    const yanchangCampus = CampusRepository.getByName("延长").value;
    const jiadinCampus = CampusRepository.getByName("嘉定").value;
    it('能打出时刻表', async () => {
        (function testCase1() {
            const timeTable = SchoolBusRepository.getByFromTo(baoshanCampus, yanchangCampus, SchoolBusRoutineType.WorkingDay)
                .map((schoolBus: SchoolBusRoutine) => {
                    return SchoolBusService.startTimeInCampus(schoolBus, baoshanCampus).value;
                })
                .map((it: Date) => it.toTimeString().slice(0, 5));
            expect(timeTable.length).equals(11);
            expect(timeTable).contains("07:00");
            expect(timeTable).contains("10:30");
            expect(timeTable).contains("12:30");
            expect(timeTable).contains("17:00");
            expect(timeTable).contains("21:40");
        })();
        (function testCase2() {
            const timeTable = SchoolBusRepository.getByFromTo(yanchangCampus, baoshanCampus, SchoolBusRoutineType.WorkingDay)
                .map((schoolBus: SchoolBusRoutine) => {
                    return SchoolBusService.startTimeInCampus(schoolBus, yanchangCampus).value;
                })
                .map((it: Date) => it.toTimeString().slice(0, 5));
            expect(timeTable.length).equals(9);
            expect(timeTable).contains("07:00");
            expect(timeTable).contains("10:00");
            expect(timeTable).contains("12:00");
            expect(timeTable).contains("13:00");
            expect(timeTable).contains("14:00");
        })();
        (function testCase3() {
            const timeTable = SchoolBusRepository.getByFromTo(yanchangCampus, jiadinCampus, SchoolBusRoutineType.WorkingDay)
                .map((schoolBus: SchoolBusRoutine) => {
                    return SchoolBusService.startTimeInCampus(schoolBus, yanchangCampus).value;
                })
                .map((it: Date) => it.toTimeString().slice(0, 5));
            expect(timeTable.length).equals(10);
            expect(timeTable).contains("07:00");
            expect(timeTable).contains("10:00");
            expect(timeTable).contains("12:00");
            expect(timeTable).contains("13:00");
            expect(timeTable).contains("14:00");
            expect(timeTable).contains("21:00");
        })();
    });
    it('能获取某一时间从某个校区到另一校区的校车', async () => {
        (function testCase1() {
            const dateTime = mergeDateTime(createDate(2018, 12, 3), createTime(6, 50));
            const bus = SchoolBusRepository.getNextByFromTo(baoshanCampus, yanchangCampus, dateTime, semester);
            expect(bus.isNull).false;
            expect(bus.value[0].startTime.toTimeString()).equals(createTime(7, 0).toTimeString());
        })()
    });
});