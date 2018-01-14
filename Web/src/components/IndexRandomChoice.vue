<template lang="pug">
  q-card
    q-card-main.text-center
      q-item
        q-item-side.text-center.flex
          q-icon(color='primary', name='gamepad', style='font-size:2rem;')
        q-item-main
          q-item-tile(label) 扔个骰子吧
          q-item-tile(sublabel) 扔一下就知道自己想要什么了
    q-card-separator
    q-card-actions
      q-btn.full-width(flat @click.native="$refs.modal.open() || randProcess(-10,6)")
        | 开始
    q-modal(ref="modal" minimized)
      q-card.no-margin
        q-card-title 
          | 投到了..
        q-card-main.text-center
          h1 
            | {{item}}
    //- .row.flex
    //-   .col12
    //-     q-select(v-bind:items="preSets" v-model="e1" label="选择预定义问题" single-line bottom)
    //-   .col12
    //-     input(hide-details name="input-1" v-model="question" single-line  label="问题")
    //-   q-card-separator
    //-   .col12(v-for="(item,key) in items" :key="item")
    //-     .row.flex
    //-       q-list
    //-         q-list-item
    //-         <v-flex xs9>
    //-           <v-text-field hide-details name="input-1" readonly single-line :value="item" label="Label Text"></v-text-field>
    //-         </v-flex>
    //-         <v-flex xs3>
    //-           <v-btn @click.native="deleteItem(key)" >删除</v-btn>
    //-         </v-flex>
    //-       </v-layout>
    //-     </v-flex>
    //-     <v-flex xs9>
    //-       <v-text-field name="input-1" label="添加选择" v-model="option"></v-text-field>
    //-     </v-flex>
    //-     <v-flex xs3>
    //-       <v-btn @click.native="onAddClick" >添加</v-btn>
    //-     </v-flex>
    //-     <v-flex xs12>
    //-       <v-btn @click.native.stop="dialog=true" block primary dark>寻找答案</v-btn>
    //-     </v-flex>
    //-   </v-layout>
    //- </v-container>
    //- <v-layout row justify-center style="position: relative;">
    //-   <v-dialog v-model="dialog" lazy absolute>
    //-     <v-card>
    //-       <v-card-title>
    //-         <div class="headline">{{question}} 答案是：</div>
    //-       </v-card-title>
    //-       <v-card-text style="text-align:center;">
    //-         <h1 class="py-5">{{item}}</h1>
    //-       </v-card-text>
    //-       <v-card-actions>
    //-         <v-btn class="green--text darken-1" flat block @click.native="randProcess(-10,items.length)">开始寻找</v-btn>
    //-       </v-card-actions>
    //-     </v-card>
    //-   </v-dialog>
    //- </v-layout>
</template>

<script>
export default {
  data() {
    return {
      e1: null,
      option: '',
      dialog: false,
      items: [1, 2, 3, 4, 5, 6],
      question: '',
      item: null,
      preSets: [
        { text: '自定义', options: [] },
        { text: '二元选择', options: ['好', '不好'] },
        { text: '去哪吃', options: ['尔美', '益新', '吾馨', '山明', '水秀'] },
        { text: '掷骰子', options: [1, 2, 3, 4, 5, 6] }
      ]
    }
  },
  watch: {
    e1: function(val) {
      this.question = val.text
      this.items = val.options
    }
  },
  methods: {
    deleteItem(key) {
      this.items.splice(key, 1)
    },
    onAddClick: function() {
      this.items.push(this.option)
      this.option = ''
    },
    randProcess(x, len) {
      // console.log(x, len)
      this.changeItem()
      if (x >= 10) return
      setTimeout(() => {
        return this.randProcess(x + 1 / len + 0.1, len)
      }, x * x)
    },
    changeItem() {
      this.item = this.items[~~(Math.random() * this.items.length)]
    }
  }
}
</script>

<style>

</style>
