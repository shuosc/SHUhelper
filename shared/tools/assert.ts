declare let process: any;

/**
 * 断言支持
 * @param condition 断言条件
 * @param message
 * @note 对于求值可能会影响系统性能的condition，可以将condition的求值过程放入lambda中传入，这样在生产环境中这个求值过程将不会被执行
 */
export function assert(condition: boolean | (() => boolean), message?: string) {
    if (process.env.NODE_ENV === 'development') {
        if (typeof condition !== "boolean") {
            assert(condition(), message);
        }
        if (condition === false) {
            throw Error('Assertion failed' + message ? ':' + message : '')
        }
    }
}