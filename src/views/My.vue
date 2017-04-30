<template>
  <div style="height:100%;">
    <scroller lock-x
              scrollbar-y
              height="-100"
              ref="scroller">
      <div>
        <group title="账号">
          <cell title="姓名"
                :value="$store.state.account.name"></cell>
          <cell title="用户名"
                :value="$store.state.account.nickname"></cell>
          <cell title="学号"
                :value="$store.state.account.card_id"></cell>
        </group>
        <group title="设置">
          <cell title="帮助"
                value="用户体验棒到不需要写帮助"></cell>
          <cell title="关于"
                value="版本 V2.2.1"></cell>
          <cell title="微信公众号"
                value="搜索添加:shuhelper"></cell>
        </group>
        <divider>BUILT WITH ❤</divider>
      </div>
    </scroller>
  </div>
</template>

<script>
import { Group, Cell, Scroller, Divider } from 'vux'

export default {
  components: {
    Group,
    Cell,
    Scroller,
    Divider
  },
  data() {
    return {
      value: 1,
      show: false,
      activateShow: false,
      cart: {
        'isempty': true
      },
      cardID: '',
      password: '',
      orderTime: '0',
      now: 0,
      currentFood: {},
      selectSpecificationShow: false,
      functions_groups: [{
        'group_tittle': '常用功能',
        'functions': [{
          'tittle': '体育',
          'icon': 'ico'
        }, {
          'tittle': '体育',
          'icon': 'ico'
        }, {
          'tittle': '体育',
          'icon': 'ico'
        }, {
          'tittle': '体育',
          'icon': 'ico'
        }, {
          'tittle': '体育',
          'icon': 'ico'
        }, {
          'tittle': '体育',
          'icon': 'ico'
        }]
      }]
    }
  },
  computed: {
  },
  methods: {
  }
}
</script>

<style>

</style>
