import { Cookie } from 'tough-cookie';
import * as Request from 'request-promise-native';

export async function postFormWithCookies(cookies: Array<Cookie>, url: string, form: any) {
  let cookiejar = Request.jar();
  for (let cookie of cookies) {
    cookiejar.setCookie(cookie.toString(), url.startsWith('https') ? 'https://' : 'http://' + cookie.domain);
  }
  return await Request.post(url, {
    jar: cookiejar,
    form: form
  });
}