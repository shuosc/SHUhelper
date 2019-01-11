export function any(array: Array<boolean>): boolean {
    for (const it of array) {
        if (it) {
            return true;
        }
    }
    return false;
}