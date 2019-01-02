import {Db, MongoClient} from "mongodb";

export let mongo: Db = null;

export async function initDB() {
    let client = await MongoClient.connect("mongo://localhost:4004", {useNewUrlParser: true});
    mongo = client.db('default');
}