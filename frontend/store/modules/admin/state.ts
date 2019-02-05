export interface State {
    token: string;
}

export const state = (): State => ({
    token: ''
});