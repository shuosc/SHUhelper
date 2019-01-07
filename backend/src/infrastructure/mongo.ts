import {Db, MongoClient} from "mongodb";

export let mongo: Db = null;

export async function initDB() {
    let client = await MongoClient.connect(process.env['MONGODB_ADDRESS'], {useNewUrlParser: true});
    mongo = client.db('default');
}