<template>
    <div>
        <v-card class="my-2">
            <v-card-title>
                一点灵息为你准备了推文：
            </v-card-title>
            <v-card-text>
                <v-container grid-list-lg style="border-style:solid;border-width:2px;border-color:#eee;" class="pa-0 ma-2" @click.stop>
                    <v-layout row style="min-height:5rem;">
                        <v-flex xs3>
                            <v-icon x-large style="height:100%;display:flex;" class="blue--text text--darken-2">public</v-icon>
                        </v-flex>
                        <v-flex xs9>
                            <a href="http://mp.weixin.qq.com/s/Mmvoyrk6kL__UzlPylgsTw" target="_blank" style="text-decoration:none;">
                                <p style="font-size:1rem;height:100%;" class="black--text text-xs-left py-2 ma-0">
                                    【SHU·一点灵息】 新学期，三个校区一起刷晨跑课外吧<br/>
                                    <span style="color:grey;font-size:0.8rem;">mp.weixin.qq.com</span>
                                </p>
                            </a>
                        </v-flex>
                    </v-layout>
                </v-container>
            </v-card-text>
        </v-card>
        <v-card class="my-2">
            <v-card-title>
                课外活动时间表
            </v-card-title>
            <v-card-text>提示：<br/>体育学院暂未发布课外活动时间表信息<br/>发布后将及时更新到这里</v-card-text>
        </v-card>
        <v-card class="my-2">
            <v-card-title>
                晨跑查询
            </v-card-title>
            <v-card-text>提示：<br/>体育学院晨跑查询接口变更<br/>暂时无法通过helper查询晨跑<br/>现在可以通过 上海大学 微信号查询晨跑相关信息<br/>我们将努力尝试恢复此功能</v-card-text>
        </v-card>

    </div>
</template>

<script>
export default {

}
</script>

<style>

</style>
