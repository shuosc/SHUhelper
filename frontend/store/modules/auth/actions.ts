import { State } from './state';
import { Types } from './types';
import axios from 'axios';
import qs from 'qs';
import { ActionContext, ActionTree } from 'vuex';
import { RootState } from '../../index';

export interface Actions<S, R> extends ActionTree<S, R> {
  doLogin: (context: ActionContext<S, R>, payload: any) => void;
  doLogout: (context: ActionContext<S, R>) => void;
}

export const actions: Actions<State, RootState> = {
  doLogin: async ({ commit }, payload: State) => {
    commit(Types.AUTH_SET_USER, {
      ...(await axios.post(`https://httpstat.us/200`, qs.stringify({
        username: payload.email,
        password: payload.password
      }))).data,
      isLogged: true
    });
  },
  doLogout: ({ commit }) => {
    commit(Types.AUTH_SET_USER, { username: '', email: '', isLogged: false });
  }
};
