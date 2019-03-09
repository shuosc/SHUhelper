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
        <v-pagination v-model="page" :length =20 circle></v-pagination>
    </div>
</template>

<script lang="ts">
import Component, {namespace} from "nuxt-class-component";
import {Vue, Watch} from 'vue-property-decorator';

@Component({
})
export default class schoolNews extends Vue{
    allNews:any;
    news:any='';
    allType=['通知公告','新闻'];
    type = '新闻';
    page:number = 1;
    isLoading:boolean = true;
    @Watch('page')
    onPageChanged(){
        if(this.type==='新闻'){
            this.news = this.$store.state.allNews.slice((this.page-1)*6,this.page*6);
        } else{this.news = this.$store.state.allNotice.slice((this.page-1)*6,this.page*6);} 
    }
    @Watch('type')
    onTypeChanged(){
        if(this.type==='新闻'){
            this.news = this.$store.state.allNews.slice((this.page-1)*6,this.page*6);
        } else{this.news = this.$store.state.allNotice.slice((this.page-1)*6,this.page*6);}
    }
    mounted(){
        this.news = this.$store.state.allNews.slice(0,6);
        this.isLoading = false;
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