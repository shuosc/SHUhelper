<template lang='pug'>
  div(class='container')
    div.card
      div.card-title.line
        p 概览
      div.card-content(style='padding: 20px;margin-bottom: 20px;')
        // mpvue的checkbox的值有问题
        // div(class='row' style='width: 100%;font-size:14px;')
        //   div.col-6(v-for='sport in sports' v-model='sportFilter' :label='sport.name' :val='sport.val' :key='sport.val')
        //     input(type='checkbox' v-model='sportFilter' :value='sport.name')
        //     label {{ sport.name }}
        // 微信原生checkbox
        checkbox-group.checkbox-group.row(style="font-size:12px;" @change="onSportChange")
          div.col-6(v-for="(sport, index) in sports" :key="index")
            label.checkbox
              checkbox(:value="sport.val") 
              | {{ sport.name }}
      
          
    div.card(v-for='(sport,i) in sportsFiltered'  :key='sport.val')
      div.card-title.line
        p {{ sport.name }}  @{{ sport.place }}
      div.card-content( v-for='(item,j) in sport.items' :key='item.day')
        div.list
          div.list-title {{ item.teacher }}
          div.list-content {{ item.day }}  {{ item.time }}
        
          

</template>
<script>
import sports from '../../../static/sports.json'
export default {
  name: 'sportCard',
  data() {
    return {
      sportFilter: [],
      sports: []
    }
  },
  created() {
    console.log(sports)
    this.sports = sports.sports
    console.log(2)
  },
  computed: {
    sportsFiltered() {
      console.log('233333')
      let filtered = this.sports
      if (this.sportFilter.length !== 0) {
        filtered = []
        this.sportFilter.forEach(item => {
          this.sports.forEach(s => {
            if (s.val === item) {
              filtered.push(s)
            }
          })
        })
      }
      return filtered
    }
  },
  methods: {
    onSportChange(e) {
      console.log(e)
      this.sportFilter = e.target.value
    }
  }
}
</script>
<style scoped>
.container {
  /* padding: 10px; */
  /* padding-right: 10px; */
  min-height: 100vh;
  /* padding-bottom: 10px; */
  /* padding-top: 10px; */
  box-sizing: border-box;
  background: #fff;
}
.card {
  padding: 0;
  margin: 10px;
  box-sizing: border-box;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 2px 0 rgba(0,0,0,0.16), 0 0 0 1px rgba(0,0,0,0.08);
} 
.card-title {
  font-size: 16px;
  padding: 15px 20px 15px 20px;
}
.card-content {
  padding: 0px;
}
.shadow {
  box-shadow: 0 2px 2px 0 rgba(0,0,0,0.16), 0 0 0 1px rgba(0,0,0,0.08);
}
.line {
  border-bottom: 1px solid rgba(0,0,0,0.08);
}
.checkbox {
  width: 10px;
}
.list {
  padding: 15px 20px 15px 20px;
  border-bottom: 1px solid rgba(0,0,0,0.08);
}
.list-title {
  font-size: 14px;
}
.list-content {
  font-size: 14px;
  color: rgba(0,0,0,0.5);
}
.name {
  font-size: 14px;
}
.place {
  font-size: 14px;
  color: #4c4c4c;
}
</style>

