import { State } from './state';
import { mutations } from './mutations';
import { actions } from './actions';

describe('store: authentication -> actions', () => {
  let state: State;
  let commit: any;
  const dispatch: any = null;
  const rootState: any = null;
  const getters: any = null;
  const rootGetters: any = null;

  beforeEach(() => {
    // mock state
    state = { client: '', username: '', email: '', isLogged: false, password: '' };

    // mock commit
    commit = (type: string, payload: State) => {
      const mutation = mutations[type];
      expect(mutation).toBeDefined();
      mutation(state, { ...payload });
    };
  });

  test('AUTH_LOGIN', async () => {
    // apply mutation
    await actions.doLogin({ state, commit, dispatch, getters, rootState, rootGetters }, {
      username: 'helmuthdu',
      email: 'helmuthdu@gmail.com'
    });
    // assert result
    expect(state.isLogged).toBe(true);
  });

  test('AUTH_LOGOUT', () => {
    // apply mutation
    actions.doLogout({ state, commit, dispatch, getters, rootState, rootGetters });
    // assert result
    expect(state.isLogged).toBe(false);
  });
});
