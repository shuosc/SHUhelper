import SignInPage from 'pages/sign-in.vue';
import { shallow } from '@vue/test-utils';

describe('Test suite for SignInPage', () => {
  let wrapper: any;

  beforeEach(() => {
    wrapper = shallow(SignInPage as any);
  });

  test('Test initial layout', () => {
    expect(wrapper.isVueInstance()).toBeTruthy();
  });

  it('should do the perform sign-in action', () => {
    wrapper.vm.email = 'user@mail.com';
    wrapper.vm.password = '12345';
    wrapper.vm.doLogin = jest.fn();

    wrapper.vm.submit();

    expect(wrapper.vm.doLogin).toBeCalledWith({ email: 'user@mail.com', password: '12345' });
  });
});
