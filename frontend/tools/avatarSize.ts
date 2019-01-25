declare const process: { client: boolean };

export function avatarSize(): number {
    if (process.client) {
        return window.innerWidth > 425 ? 60 : 40;
    }
    return 50;
}