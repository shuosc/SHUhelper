<template>
    <div>
        <v-select :items="allType" v-model="type"></v-select>
        <v-progress-linear :indeterminate="true" v-if="isLoading"></v-progress-linear>
        <v-list v-for="item in news" :key="item.title" v-else dense>
            <a :href="item.link" target="_blank" id="article_link">
            <v-list-tile>
                <v-list-tile-title>
                    {{item.title}}
                </v-list-tile-title>
                <v-list-tile-action-text id="article_data">
                    {{item.data}}
                </v-list-tile-action-text>
            </v-list-tile>
            </a>
        </v-list>
        <v-pagination v-model="page" :length = 50 circle></v-pagination>
    </div>
</template>

<script lang="ts">
import Component, {namespace} from "nuxt-class-component";
import {Vue, Watch} from 'vue-property-decorator';
 
@Component({

})
export default class schoolNews extends Vue{
    allNews:any;
    news:any;
    allType=['通知公告','新闻'];
    type = '新闻';
    page:number = 1;
    isLoading:boolean = true;
    @Watch('page')
    onPageChanged(){
        this.isLoading = true
        if(this.page>5){
            this.$axios.$post('/api/fetchNews',{type:this.type,startIndex:(this.page-1)*6,endIndex:this.page*6})
                .then(res=>{
                    this.news=res
                    this.isLoading = false;
                })
        } else {
            this.news = this.allNews.slice((this.page-1)*6,this.page*6)
            this.isLoading = false;
        }
    }
    @Watch('type')
    onTypeChanged(){
        this.isLoading = true;
        this.$axios.$post('/api/fetchNews',{type:this.type,startIndex:0,endIndex:30})
            .then(res=>{
                this.allNews = res;
                this.page = 1;
                this.news = this.allNews.slice(0,6);
                this.isLoading = false;
            })
    }
    mounted(){
        this.$axios.$post('/api/fetchNews',{type:this.type,startIndex:0,endIndex:30})
            .then(res=>{
            this.allNews = res;
            this.news=this.allNews.slice(0,6)
            this.isLoading = false;
            })
    }
}
</script>

<style scoped>
#article_link{
    text-decoration: none;
    color:white
}
#article_data{
    white-space: nowrap;
}
</style>
