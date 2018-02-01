import os
from instance.config import TESTING_CARD_ID, TESTING_PASSWORD
from time import sleep

index_url = os.getenv('INDEX_URL', 'http://0.0.0.0:8080/index')

use_browser = os.getenv('WITH_UI', 1)

if use_browser:
    from selenium.webdriver import Chrome as Browser
else:
    from selenium.webdriver import PhantomJS as Browser


def try_login_with(browser, username, password):
    # 用户看见了账号密码输入框
    input_boxes = browser.find_elements_by_class_name('q-card')[2]
    input_student_id = input_boxes.find_elements_by_tag_name('input')[0]
    input_password = input_boxes.find_elements_by_tag_name('input')[1]
    submit_button = input_boxes.find_element_by_tag_name('button')
    input_student_id.send_keys(username)
    input_password.send_keys(password)
    submit_button.click()
    sleep(5)
    return '首页' in browser.find_element_by_class_name('q-toolbar-title').text


def test_login():
    browser = Browser()
    # 用户打开了主页
    browser.get(index_url)
    left_bar = browser.find_element_by_class_name('layout-aside-left')
    # 用户看见了登录按键
    login_button = left_bar.find_element_by_class_name('q-card-main')
    assert '登录' in login_button.text
    # 用户点击了登录
    login_button.click()
    sleep(1)
    # 用户尝试用不正确的密码登录
    success = try_login_with(browser, TESTING_CARD_ID, '000000')
    # 并没有登录成功
    assert not success
    # 用户尝试输入正确的密码
    browser.refresh()
    sleep(1)
    success = try_login_with(browser, TESTING_CARD_ID, TESTING_PASSWORD)
    assert success
    # 登录成功
    assert '首页' in browser.find_element_by_class_name('q-toolbar-title').text
    browser.close()


def test_saysth():
    browser = Browser()
    # 用户打开了主页
    browser.get(index_url)
    left_bar = browser.find_element_by_class_name('layout-aside-left')
    # 用户看见了登录按键
    login_button = left_bar.find_element_by_class_name('q-card-main')
    assert '登录' in login_button.text
    # 用户点击了登录
    login_button.click()
    sleep(1)
    # 用户登录了网站
    assert try_login_with(browser, TESTING_CARD_ID, TESTING_PASSWORD)
    # 用户点击了"广场"
    browser.find_element_by_xpath('//*[@id="q-app"]/div/aside/div[1]/div[2]/div[3]/div[2]/div').click()
    # 用户点击了"+"按钮
    browser.find_element_by_css_selector(
        'div.layout-page-container.transition-generic > main > div:nth-child(1) > div.z-fixed.fixed-bottom-right > button').click()
    sleep(1)
    # 用户输入了一些话
    browser.find_element_by_xpath(
        '/html/body/div[3]/div/div/div[2]/div[1]/div/div/div/div/a/div[2]/div[2]/textarea').send_keys('测试')
    # 用户点击了发布
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div/button[2]/span').click()
    sleep(1)
    # 用户看见了自己的帖子
    the_post = browser.find_element_by_css_selector(
        '#q-app > div > div.layout-page-container.transition-generic > main > div:nth-child(1) > div.q-infinite-scroll > div.q-infinite-scroll-content > div:nth-child(3)')
    post_text = the_post.text
    assert '测试' in post_text
    # 用户点击了删除
    the_post.find_element_by_tag_name('button').click()
    sleep(1)
    browser.find_element_by_class_name('modal-buttons').find_elements_by_tag_name('button')[1].click()
    sleep(1)
    # 用户不再能看见了自己的帖子了
    try:
        the_post = browser.find_element_by_css_selector(
            '#q-app > div > div.layout-page-container.transition-generic > main > div:nth-child(1) > div.q-infinite-scroll > div.q-infinite-scroll-content > div:nth-child(3)')
    except:
        pass
    else:
        post_text = the_post.text
        assert '测试' not in post_text
    browser.close()
