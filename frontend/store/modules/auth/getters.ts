import { RootState } from '../../index';
import { State } from './state';
import { GetterTree } from 'vuex';

export const getters: GetterTree<State, RootState> = {
  isLogged: (state: State) => {
    return state.isLogged;
  }
};
