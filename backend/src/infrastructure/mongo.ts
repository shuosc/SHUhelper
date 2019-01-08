import {Db, MongoClient, ObjectID} from "mongodb";
import {clone} from "../../../shared/tools/clone";

export let mongo: Db = null;

/**
 * 初始化数据库
 * 在一切其他代码调用之前调用
 */
export async function initDB() {
    let client = await MongoClient.connect(process.env['MONGODB_ADDRESS'], {useNewUrlParser: true});
    mongo = client.db('default');
}

/**
 * 移除某个对象上的 _id 字段
 */
export function removeId(object: { _id: ObjectID }) {
    let newObject = clone(object);
    delete newObject._id;
    return newObject;
}