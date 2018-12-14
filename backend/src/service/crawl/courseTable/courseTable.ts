import { Cookie } from 'tough-cookie';
import { postFormWithCookies } from '../../../infrastructure/request';
import * as Cheerio from 'cheerio';
import * as Entities from 'html-entities';
import { Course, ICourse } from '../../../model/course';
import { currentSemester } from '../../../model/semester';
import { getOrCreateTeacherByName } from '../../../model/teacher';
import { ClassType, IClass, IClassLocation, IClassTime } from '../../../../../shared/model/course';

const entities = new Entities.XmlEntities();

export function fetchCoursePage(studentId: string, cookies: Array<Cookie>): Promise<string> {
  return postFormWithCookies(cookies, 'http://xk.autoisp.shu.edu.cn/StudentQuery/CtrlViewQueryCourseTable', {
    studentNo: process.env.STUDENT_ID
  });
}

const WEEK_CHINESE_TO_NUMBER_MAP = new Map<string, number>([
  ['一', 1],
  ['二', 2],
  ['三', 3],
  ['四', 4],
  ['五', 5]
]);

function parseClassTime(day: string, sectorRange: string): IClassTime {
  const [from, to] = sectorRange.split('-');
  return {
    day: WEEK_CHINESE_TO_NUMBER_MAP.get(day.trim()),
    startSector: parseInt(from),
    endSector: parseInt(to)
  };
}

function parseClassPlace(place: string, campus: string): IClassLocation {
  const regex = /(.*?)(\d+)/;
  const buildingAndRoom = regex.exec(place);
  let building = '';
  let room = '';
  if (buildingAndRoom !== null) {
    building = buildingAndRoom[1];
    room = buildingAndRoom[2];
  } else {
    building = place;
  }
  return {
    campus: campus,
    building: building,
    roomNumber: room
  };
}

function parseClassType(infoString: string): ClassType {
  if (infoString.includes('研讨')) {
    return ClassType.discussion;
  } else if (infoString.includes('上机')) {
    return ClassType.computer;
  }
  return ClassType.normal;
}

async function parseClasses(dayAndSectors: string, place: string, campus: string): Promise<Array<IClass>> {
  let result: Array<IClass> = [];
  const regex = /([一二三四五])((\d+)-(\d+))([^一二三四五]*)/g;
  let match = regex.exec(dayAndSectors);
  while (match !== null) {
    result.push({
      time: parseClassTime(match[1], match[2]),
      location: await parseClassPlace(place, campus),
      type: await parseClassType(match[5])
    });
    match = regex.exec(dayAndSectors);
  }
  return result;
}

async function parseCourse(cols: Array<string>): Promise<ICourse> {
  let result = await Course.findOne({ id: cols[1] }).exec();
  if (result === null) {
    const hasManyTeacher = cols[4][cols[4].length - 1] === '等';
    const teacher = await getOrCreateTeacherByName(hasManyTeacher ? cols[4].slice(0, -1) : cols[4]);
    const semester = await currentSemester();
    const classes = await parseClasses(cols[6], cols[7], cols[8]);
    result = await Course.create({
      id: cols[1],
      name: cols[2],
      teacher: teacher,
      manyTeacher: hasManyTeacher,
      semester: semester,
      classes: classes
    });
    result = await result.save();
  }
  return result;
}

export async function parseCoursePage(page: string): Promise<Array<ICourse>> {
  const $ = Cheerio.load(page, { ignoreWhitespace: true });
  let courses: Array<ICourse> = [];
  for (let index = 3; ; ++index) {
    let row = $($('tr')[index]);
    let cols = [];
    row.find('td').each((_, element: CheerioElement) => {
      cols.push(entities.decode($(element).html().trim()));
    });
    if (cols.length !== 11) {
      break;
    }
    courses.push(await parseCourse(cols));
  }
  return courses;
}

















