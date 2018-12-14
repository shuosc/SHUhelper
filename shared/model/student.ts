import { ICourse } from './course';

export interface IStudent {
  id: string,
  name: string,
  courses: Array<ICourse>
}