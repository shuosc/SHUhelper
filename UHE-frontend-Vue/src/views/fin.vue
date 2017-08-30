<template>
  <div>
    <v-card>
      <v-card-title>学生信息</v-card-title>
      <v-card-text>
        姓名 证件类型 证件号 欠缴金额

      </v-card-text>
    </v-card>
    <v-tabs light fixed centered>
      <v-tabs-bar slot="activators" class="white">
        <v-tabs-slider class="yellow"></v-tabs-slider>
        <v-tabs-item v-for="i in items" :key="i" :href="'#tab-' + i">
          {{ i }}
        </v-tabs-item>
      </v-tabs-bar>
      <v-tabs-content id="tab-缴费情况">
        <v-card flat>
          <!-- <v-card-text> -->
          <v-expansion-panel expand>
            <v-expansion-panel-content>
              <div slot="header">2016-2017年学费-本科生收费套类</div>
              <v-card flat>
                <v-card-text class="white lighten-3">
                  <v-layout row wrap>
                    <v-flex xs3>应收金额 </v-flex>
                    <v-flex xs3></v-flex>
                    <v-flex xs3>减免金额 </v-flex>
                    <v-flex xs3></v-flex>
                    <v-flex xs3>缓缴金额 </v-flex>
                    <v-flex xs3></v-flex>
                    <v-flex xs3>已交费金额 </v-flex>
                    <v-flex xs3></v-flex>
                    <v-flex xs3>欠费金额 </v-flex>
                    <v-flex xs3></v-flex>
                    <v-flex xs3>待退金额 </v-flex>
                    <v-flex xs3></v-flex>
                  </v-layout>
                </v-card-text>
                <v-card-actions>
                  <v-btn block>查看明细</v-btn>

                </v-card-actions>
              </v-card>
            </v-expansion-panel-content>
            <v-expansion-panel-content>
              <div slot="header">2016年教材费-本科生收费套类</div>
              <v-card>
                <v-card-text class="grey lighten-3">Lorem ipsum dolor sit amet, consectetur
                  adipiscing elit, sed do eiusmod tempor
                  incididunt ut labore et dolore magna
                  aliqua. Ut enim ad minim veniam,
                  quis nostrud exercitation ullamco
                  laboris nisi ut aliquip ex ea commodo
                  consequat.
                </v-card-text>
              </v-card>
            </v-expansion-panel-content>
          </v-expansion-panel>
          <!-- </v-card-text> -->
        </v-card>
      </v-tabs-content>
      <v-tabs-content id="tab-缴费记录">
        <v-card flat>

          <v-card-text>
            <v-expansion-panel>
              <v-expansion-panel-content v-for="(item,i) in 5"
                :key="i">
                <div slot="header">Item</div>
                <v-card>
                  <v-card-text class="grey lighten-3">Lorem ipsum dolor sit amet, consectetur
                    adipiscing elit, sed do eiusmod
                    tempor incididunt ut labore et
                    dolore magna aliqua. Ut enim ad
                    minim veniam, quis nostrud exercitation
                    ullamco laboris nisi ut aliquip
                    ex ea commodo consequat.</v-card-text>
                </v-card>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-card-text>
        </v-card>
      </v-tabs-content>
      <v-tabs-content id="tab-欠缴情况">
        <v-card flat>
          <v-card-text>{11111</v-card-text>
        </v-card>
      </v-tabs-content>
    </v-tabs>
  </div>
</template>

<script>
export default {
  data () {
    return {
      items: ['缴费情况', '缴费记录', '欠缴情况']
    }
  }
}
</script>

<style>

</style>
