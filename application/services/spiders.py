def get_shu_info_single():
    category = request.args['category']
    msg_id = request.args['msgID']
    url = 'http://www.shu.edu.cn/info/{}/{}.htm'.format(category, msg_id)
    page_content = requests.get(url)
    soup = BeautifulSoup(page_content.text, "html.parser")
    contents = soup.find(id="vsb_content").table.tr.td.contents
    return jsonify(content=str(contents[2]))