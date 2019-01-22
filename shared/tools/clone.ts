export function clone<T>(obj: T): T {
  let copy;

  if (null == obj || 'object' != typeof obj) return obj;

  // Handle Date
  if (obj instanceof Date) {
    copy = new Date();
    copy.setTime(obj.getTime());
    return copy as any as T;
  }

  // Handle Array
  if (obj instanceof Array) {
    copy = [];
    for (let i = 0, len = obj.length; i < len; i++) {
      copy[i] = clone(obj[i]);
    }
    return copy as any as T;
  }

  // Handle Object
  if (obj instanceof Object) {
    copy = {};
    for (let attr in obj) {
      if (obj.hasOwnProperty(attr))
        (copy as any)[attr] = clone(obj[attr]);
    }
    return copy as any as T;
  }

  throw new Error('Unable to copy obj! Its type isn\'t supported.');
}
