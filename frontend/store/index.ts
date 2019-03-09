import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';
import * as url from 'url';
import * as Cheerio from 'cheerio'
import * as student from './modules/student';
import * as courses from './modules/course';
import * as semesters from './modules/semester';
import * as admin from './modules/admin';
import * as root from './root';

Vue.use(Vuex);

interface ModulesStates {
    student: student.State;
    courses: courses.State;
    semester: semesters.State;
    admin: admin.State;
}

export type RootState = root.State & ModulesStates;
export default () => new Vuex.Store({
    state: root.state() as any,
    getters: root.getters,
    mutations: root.mutations,
    actions:{
        async nuxtServerInit({commit},{store}){
            let allNews:any = [];
            let allNotices:any=[];
            const host = 'http://www.jwc.shu.edu.cn';
            const allNewsLink:Array<string> = ['http://www.jwc.shu.edu.cn/index/tzgg.htm'];
            const allNoticeLink:Array<string> = ['http://www.jwc.shu.edu.cn/index/xw.htm'];
            for(let i = 50;i>=49;i--){
                allNewsLink.push(`http://www.jwc.shu.edu.cn/index/tzgg/${i}.htm`)
                allNoticeLink.push(`http://www.jwc.shu.edu.cn/index/xw/${i-32}.htm`)
            }
            let config = [
                {
                    type:'news',
                    link:allNewsLink,
                    info:allNews
                },
                {
                    type:'notice',
                    link:allNoticeLink,
                    info:allNotices
                }
            ]
            for(let obj of config){
                for(let link of obj.link){
                    let respond:any;
                    await axios.get(link).then(res=>respond = res)
                    const $ =Cheerio.load(respond.data)
                    let list:Array<any> =$('#dnn_ctr43516_ArticleList__ctl0_ArtDataList__ctl1_titleLink1')
                        .map(function(index:number, ele:any) {
                            return {
                                title: $(ele).attr('title'),
                                link: $(ele).attr('href'),
                                data: $('#dnn_ctr43516_ArticleList__ctl0_ArtDataList__ctl1_Label6').eq(index).text(),
                            };
                        })
                        .get();
                    Promise.all(
                        list.map((item) => {
                            const itemUrl = url.resolve(host, item.link);
                            const single = {
                                title: item.title,
                                link: itemUrl,
                                data:item.data
                            };
                        return Promise.resolve(single);
                        })
                    ).then(res=>{obj.info.push(...res)});  
                }
            let before = obj.info[0];
            //对数据进行筛选
            for(let index=1;index<obj.info.length;index++){
                if((parseInt(obj.info[index].data.replace(/-/g,''))<=parseInt(before.data.replace(/-/g,'')))&&(obj.info[index].title!==before.title)){
                    before = obj.info[index];
                } else{
                    obj.info.splice(index,1);
                    index--;
                }
            }
        }
            store.state.allNews = allNews;
            store.state.allNotice = allNotices;
        }
    },
    modules: {
        [student.name]: student,
        [courses.name]: courses,
        [semesters.name]: semesters,
        [admin.name]: admin,
    }
});