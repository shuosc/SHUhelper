interface User {
    name: string;
    token: string;
}

export interface State {
    user: User | null;
}

export const state = (): State => ({
    user: null
});