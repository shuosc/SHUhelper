declare let process: any;

/**
 * 断言支持
 * @note 对于求值可能会影响系统性能的condition，
 *       可以wrap进闭包使用下面的assertFunction，
 *       这样在生产环境中这个求值过程将不会被执行
 */
export function assert(condition: boolean, message?: string) {
    if (process.env.NODE_ENV === 'development' && condition === false) {
        throw Error('Assertion failed' + (message !== undefined ? `:${message}` : ''))
    }
}

/**
 * 对无参函数进行断言
 */
export function assertFunction(condition: () => boolean, message?: string) {
    if (process.env.NODE_ENV === 'development') {
        assert(condition(), message);
    }
}