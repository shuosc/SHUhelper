import "mocha"
import {expect} from "chai";
import {randomSelect} from "./randomSelect";

describe('随机选取测试', async () => {
    it('能随机选取数组中的值', async () => {
        const array = [1, 2, 3, 4, 5];
        let result = [];
        // 脸黑者请勿执行此测试
        for (let i = 0; i < 10000; ++i) {
            result.push(randomSelect(array));
        }
        expect(result).contains(1);
        expect(result).contains(2);
        expect(result).contains(3);
        expect(result).contains(4);
        expect(result).contains(5);
        expect(result).not.contains(0);
        expect(result).not.contains(6);
    });
});