import Vue from 'vue';
import Vuex from 'vuex';
import * as auth from './modules/auth';
import * as root from './root';

Vue.use(Vuex);

// More info about store: https://vuex.vuejs.org/en/core-concepts.html
// See https://nuxtjs.org/guide/vuex-store#classic-mode
// structure of the store:
// types: Types that represent the keys of the mutations to commit
// state: The information of our app, we can get or update it.
// getters: Get complex information from state
// action: Sync or async operations that commit mutations
// mutations: Modify the state
interface ModulesStates {
  auth: auth.State;
}

export type RootState = root.State & ModulesStates;

export default () => new Vuex.Store({
  state: root.state() as any,
  getters: root.getters,
  mutations: root.mutations,
  actions: root.actions as any,
  modules: {
    [auth.name]: auth
  }
});
