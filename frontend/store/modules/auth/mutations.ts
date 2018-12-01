import { State } from './state';
import { Types } from './types';
import { MutationTree } from 'vuex';

export const mutations: MutationTree<State> = {
  [Types.AUTH_SET_USER]: (state: State, payload: State) => {
    state.username = payload.username;
    state.email = payload.email;
    state.isLogged = payload.isLogged;
  }
};
