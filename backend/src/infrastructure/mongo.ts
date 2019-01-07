import {Db, MongoClient, ObjectID} from "mongodb";
import {clone} from "../../../shared/tools/clone";

export let mongo: Db = null;

export async function initDB() {
    let client = await MongoClient.connect(process.env['MONGODB_ADDRESS'], {useNewUrlParser: true});
    mongo = client.db('default');
}

export function removeId(object: { _id: ObjectID }) {
    let newObject = clone(object);
    delete newObject._id;
    return newObject;
}