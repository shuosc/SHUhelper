import * as Cheerio from 'cheerio';
import * as url from 'url';


const host = 'http://www.jwc.shu.edu.cn';

const config = {
    '通知公告': 'http://www.jwc.shu.edu.cn/index/tzgg.htm',
    '新闻':  'http://www.jwc.shu.edu.cn/index/xw.htm'
};
export async function fetchNews(that:any,type:string,startIndex:number,endIndex:number) {
    const API_PROXY = 'https://bird.ioliu.cn/v1/?url=';
    let link:string;
    if(type === "notice"){
        if(startIndex>=30){
            link = `http://www.jwc.shu.edu.cn/index/tzgg/${51-Math.floor(startIndex/30)}.htm`;
            startIndex =startIndex %30;
            endIndex = endIndex %30 === 0 ? 30:endIndex%30;
        } else {link = 'http://www.jwc.shu.edu.cn/index/tzgg.htm'}
    } else {
        if(startIndex>=30){
            link = `http://www.jwc.shu.edu.cn/index/xw/${19-Math.floor(startIndex/30)}.htm`;
            startIndex =startIndex %30;
            endIndex = endIndex %30 === 0 ? 30:endIndex%30;
        } else {link = 'http://www.jwc.shu.edu.cn/index/xw.htm'}
    }
    const respond = await (that.$axios as any)({
        method:'get',
        url:API_PROXY+link,
    })
    const $ = Cheerio.load(respond.data);
    let list:Array<any> =$('#dnn_ctr43516_ArticleList__ctl0_ArtDataList__ctl1_titleLink1').slice(startIndex,endIndex)
        .map(function(index, ele) {
            return {
                title: $(ele).attr('title'),
                link: $(ele).attr('href'),
                data: $('#dnn_ctr43516_ArticleList__ctl0_ArtDataList__ctl1_Label6').eq(index+startIndex).text(),
            };
        })
        .get();
    const all:Promise<any> = Promise.all(
        list.map((item) => {
            const itemUrl = url.resolve(host, item.link);
            const single = {
                title: item.title,
                link: itemUrl,
                data:item.data
            };
            return Promise.resolve(single);
        })
    )
    return all;
};