import { MutationTree } from 'vuex';
import { State } from './state';
import { Types } from './types';

export const mutations: MutationTree<State> = {
  [Types.DATE_SET]: (state: State, payload: State) => {
    state.year = payload.year;
    state.week = payload.week;
    state.term = payload.term;
    state.day = payload.day;
  }
};
