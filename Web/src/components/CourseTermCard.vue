<template lang="pug">
  q-card.no-margin(style="width:80vw;" v-if="course")
    q-card-title
      | {{course.name}}-{{classes[0].term|term}}
    q-card-main.no-padding
      q-tabs(inverted v-model="classTab")
        q-tab( v-for="(courseClass,index) in classes" slot="title",
        :name="courseClass._id.$oid",:key="courseClass._id.$oid" ,
        :label="courseClass.teacher_no+'班'")
        q-tab-pane(v-for="(courseClass,index) in classes",
        :key="courseClass._id.$oid",:name="courseClass._id.$oid")
          q-list( inset-separator no-border)
            q-item
              q-item-side
                | 教师
              q-item-main.text-center
                | {{courseClass.teacher_name}}({{courseClass.teacher_no}})
            q-item
              q-item-side
                | 时间
              q-item-main.text-center(style="font-size:0.7rem;")
                | {{courseClass.time}}
            q-item
              q-item-side
                | 地点
              q-item-main.text-center(style="font-size:0.8rem;")
                | {{courseClass.place}}
            q-item
              q-item-side
                | 答疑
              q-item-main.text-center(style="font-size:0.8rem;")
                | {{courseClass.q_time}} @{{courseClass.q_place}}
  
</template>

<script>
import { QTabs, QTabPane, QTab } from 'quasar'
export default {
  props: {
    classes: Array,
    course: Object
  },
  components: {
    QTabs,
    QTabPane,
    QTab
  },
  data() {
    return {
      classTab: ''
    }
  },
  created: function() {
    this.classTab = this.classes[0]._id.$oid
  }
}
</script>

<style>

</style>
