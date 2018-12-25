import {Db, MongoClient} from "mongodb";

export let mongodb: Db = null;

export async function initDB() {
    let client = await MongoClient.connect("mongodb://localhost:4004", {useNewUrlParser: true});
    mongodb = client.db('default');
}