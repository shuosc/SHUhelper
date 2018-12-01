import HomePage from 'pages/index.vue';
import { shallow } from '@vue/test-utils';

const $route = {
  path: '/some/path',
  query: {
    apikey: '',
    user: ''
  }
};

describe('Test suite for HomePage', () => {
  test('Test initial layout', () => {
    const wrapper = shallow(HomePage as any, {
      mocks: {
        $route
      }
    });

    expect(wrapper.isVueInstance()).toBeTruthy();
  });
});
