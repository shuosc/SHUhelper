import {Db, MongoClient} from "mongodb";

export let mongodb: Db;

(async () => {
    let client = await MongoClient.connect("mongodb://localhost:4004", {useNewUrlParser: true});
    mongodb = client.db('default');
})();