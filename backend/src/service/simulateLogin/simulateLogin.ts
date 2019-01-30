import * as Request from 'request-promise-native';
import * as Cheerio from 'cheerio';
import * as Tough from 'tough-cookie';
import {CookieJar} from "request";

async function postWithSaml(url: string, samlRequest: string, relayState: string, jar: CookieJar) {
    await Request.post(url, {
        jar: jar,
        form: {
            SAMLRequest: samlRequest,
            RelayState: relayState
        },
        simple: false,
        followAllRedirects: true
    });
}

/**
 * 模拟登录
 * @param fromURL 要登录的网站的url
 * @return 拿到的cookie，可以用于下次请求这个网站的内容
 */
export async function simulateLogin(fromURL: string, studentId: string, password: string): Promise<Array<Tough.Cookie>> {
    let cookiejar = Request.jar();
    let $ = Cheerio.load(await Request.get(fromURL, {
        jar: cookiejar
    }));
    // Silly WebStorm! It is NOT JQuery!!!
    // noinspection JSJQueryEfficiency
    let form = $('form').serializeArray();
    await postWithSaml('https://sso.shu.edu.cn/idp/profile/SAML2/POST/SSO', form[0].value, form[1].value, cookiejar);
    $ = Cheerio.load(await Request.post('https://sso.shu.edu.cn/idp/Authn/UserPassword', {
        jar: cookiejar,
        form: {
            j_username: studentId,
            j_password: password
        },
        simple: false,
        followAllRedirects: true
    }));
    // noinspection JSJQueryEfficiency
    form = $('form').serializeArray();
    await postWithSaml('http://oauth.shu.edu.cn/oauth/Shibboleth.sso/SAML2/POST', form[1].value, form[0].value, cookiejar);
    await Request.get(fromURL, {
        jar: cookiejar
    });
    return cookiejar.getCookies(fromURL);
}
