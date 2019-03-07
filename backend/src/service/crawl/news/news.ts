import * as Cheerio from 'cheerio';
import * as url from 'url';
import * as Request from 'request-promise-native';


const host = 'http://www.jwc.shu.edu.cn';
/**
 *  爬取教务处网站公告新闻
 * @param type 数据类型
 * @param startIndex 起始条数
 * @param endIndex 终止条数
 */
export async function fetchNews(type:string,startIndex:number,endIndex:number) {
    let link:string;
    if(type == "新闻"){
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
    let respond = await Request.get(link)
    console.log(link);
    console.log(startIndex)
    const $ = Cheerio.load(respond);
    let list:Array<any> =$('#dnn_ctr43516_ArticleList__ctl0_ArtDataList__ctl1_titleLink1').slice(startIndex,endIndex)
        .map(function(index:number, ele:CheerioElement) {
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