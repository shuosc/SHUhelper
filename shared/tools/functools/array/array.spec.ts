import {find, findBefore, findIndex, findIndexBefore} from "./array";
import {expect} from 'chai';

describe('Array 测试', async () => {
    it('find能正常工作', async () => {
        expect(find([1, 2, 3, 4, 5], it => it % 2 === 1).value).equals(1);
        expect(find([1, 2, 3, 4, 5], it => it % 2 === 0).value).equals(2);
        expect(find([1, 2, 3, 4, 5], it => it === 6).isNull).true;
    });
    it('findIndex能正常工作', async () => {
        expect(findIndex([1, 2, 3, 4, 5], it => it % 3 === 0).value).equals(2);
        expect(findIndex([1, 2, 3, 4, 5], it => it % 4 === 0).value).equals(3);
        expect(findIndex([1, 2, 3, 4, 5], it => it === 6).isNull).true;
    });
    it('findBefore', async () => {
        expect(findBefore([1, 2, 3, 4, 5], it => it % 2 === 1).isNull).true;
        expect(findBefore([1, 2, 3, 4, 5], it => it % 2 === 0).value).equals(1);
    });
    it('findBeforeIndex能正常工作', async () => {
        expect(findIndexBefore([1, 2, 3, 4, 5], it => it % 3 === 0).value).equals(1);
        expect(findIndexBefore([1, 2, 3, 4, 5], it => it % 4 === 0).value).equals(2);
    });
});