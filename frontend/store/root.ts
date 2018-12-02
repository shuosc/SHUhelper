import { ActionContext, ActionTree, GetterTree, MutationTree } from 'vuex';
import { RootState } from '.';

export const types = {};

export interface State {
  version: string;
}

export const state = (): State => ({
  version: '1.0.0'
});

export const getters: GetterTree<State, RootState> = {};

export interface Actions<S, R> extends ActionTree<S, R> {
  getVersion(context: ActionContext<S, R>): void;
}

export const actions: Actions<State, RootState> = {
  async getVersion(context: ActionContext<State, RootState>) {
    return context.state.version;
  }
};

export const mutations: MutationTree<State> = {};
