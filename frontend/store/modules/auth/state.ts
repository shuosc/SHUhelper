export interface State {
  username: string;
  email: string;
  client: string;
  isLogged?: boolean;
  password: string;
}

export const state = (): State => ({
  username: '',
  email: '',
  client: '',
  isLogged: false,
  password: ''
});
