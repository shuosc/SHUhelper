<template>
  <div>
    <v-container fluid class="px-2 mx-2">
      <v-layout row wrap>
        <!-- <v-flex xs12>
                    <v-subheader>预设问题集</v-subheader>
                  </v-flex> -->
        <v-flex xs12>
          <v-select v-bind:items="preSets" v-model="e1" label="选择预定义问题" single-line bottom></v-select>
        </v-flex>
        <!-- <v-flex xs12>
                    <v-subheader>自定义问题</v-subheader>
                  </v-flex> -->
        <v-flex xs12 v-for="(item,key) in items" :key="item">
          <v-layout row wrap>
            <v-flex xs6>
              <v-text-field hide-details name="input-1" readonly single-line :value="item" label="Label Text" id="testing"></v-text-field>
            </v-flex>
            <v-flex xs6>
              <v-btn @click.native="deleteItem(key)">删除</v-btn>
            </v-flex>
          </v-layout>
        </v-flex>
        <v-flex xs6>
          <v-text-field name="input-1" label="添加选择" id="testing" v-model="option"></v-text-field>
        </v-flex>
        <v-flex xs6>
          <v-btn @click.native="onAddClick">添加</v-btn>
        </v-flex>
      </v-layout>
    </v-container>
    <v-layout row justify-center style="position: relative;">
      <v-dialog v-model="dialog" lazy absolute>
        <v-btn primary dark slot="activator">寻找答案</v-btn>
        <v-card>
          <v-card-title>
            <div class="headline">你问题的答案是：</div>
          </v-card-title>
          <v-card-text style="text-align:center;">
            <h1 class="py-5">{{item}}</h1>
          </v-card-text>
          <v-card-actions>
            <v-btn class="green--text darken-1" flat block @click.native="randProcess(-10,items.length)">开始寻找</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-layout>
  </div>
</template>

<script>
export default {
  data () {
    return {
      e1: null,
      option: '',
      dialog: false,
      items: ['好', '不好'],
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
    e1: function (val) {
      this.items = val.options
    }
  },
  methods: {
    deleteItem (key) {
      this.items.splice(key, 1)
    },
    onAddClick: function () {
      this.items.push(this.option)
      this.option = ''
    },
    randProcess (x, len) {
      // console.log(x, len)
      this.changeItem()
      if (x >= 10) return
      setTimeout(() => { return this.randProcess(x + 1 / len + 0.1, len) }, x * x)
    },
    changeItem () {
      this.item = this.items[~~(Math.random() * this.items.length)]
    }
  }
}
</script>

<style>

</style>
