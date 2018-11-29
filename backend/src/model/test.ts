// this is only a tempory test to make sure we really connected to our db
// will be removed soon
import { Document, model, Model, Schema } from 'mongoose';

interface ITest extends Document {
  name: string
}

export const TestSchema: Schema = new Schema({
  name: { type: String, required: true }
});

export const Test: Model<ITest> = model('Test', TestSchema);

