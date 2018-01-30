<template lang="pug">
  div 
    blockquote(style="margin:1rem;")
      small
        | 现在，你也可以在这里直接进行选课退课，查看课程排名
        br
        | 该功能目前处于测试阶段，如果出现问题请尝试刷新
    q-list(no-border)
      q-list-header
        | 17-18春季学期
      q-item.justify-between
        q-btn(@click="getRank" icon="refresh") 刷新
        q-btn(@click="courseAddModal=true" icon="add") 选课
        q-btn(@click="quitCourses" icon="clear" :disable="!selectedCourses.length") 退课
      q-item(v-for="(course,index) in courses")
        q-item-side
            q-checkbox(v-model="courses[index].checked")
        q-item-main
          q-item-tile(label) {{course.name}}-{{course.teacher}}
          q-item-tile(sublabel) {{course.no}}-{{course.class}}
          q-item-tile(sublabel) 当前排名{{course.rank}}，已选{{course.enroll}}人，容量{{course.capacity}}人
        //- q-item-side
            q-btn(@click="showDetail(course)" flat icon="visibility") 
    q-modal(v-model="courseAddModal" minimized :content-css="{minWidth: '80vw'}")
      q-card-main
        q-field(:count="10" )
          mt-field(placeholder="课程号" v-model="course.no")
        q-field( :count="450")
          mt-field(placeholder="教师号" v-model="course.class")
        q-btn.full-width(@click="selectCourse")
          | 添加课程
    //- q-modal(v-modal=)

    
</template>
<script>
import { QChip, QRating, QCheckbox, Loading, Toast, Dialog } from 'quasar'
import CourseTermCard from '@/CourseTermCard'
import { mapGetters } from 'vuex'
export default {
  components: {
    QChip,
    CourseTermCard,
    QCheckbox,
    QRating
  },
  data() {
    return {
      course: {
        no: '',
        class: ''
      },
      loading: false,
      courses: [],
      courseSearchModal: false,
      evalationModal: false,
      evaluations: [],
      classes: null,
      dialog: false,
      courseAddModal: false,
      selectedCorses: [],
      result: {}
    }
  },
  mounted() {
    this.getRank()
  },
  deactivated: function() {
    Loading.hide()
  },
  computed: {
    ...mapGetters(['user']),
    selectedCourses: function() {
      let filtered = this.courses.filter((element, index, array) => {
        return element.checked
      })
      return filtered
    }
  },
  methods: {
    getRank() {
      Loading.show()
      this.$http
        .post(`/api/courses/manage/rank`, {
          card_id: this.user.cardID,
          password: this.user.password
        })
        .then(response => {
          this.courses = []
          for (let course of response.data) {
            course.checked = false
            this.courses.push(course)
          }
          Loading.hide()
        })
        .catch(err => {
          Loading.hide()
          Toast.create('获取选课信息失败，请重新尝试')
          console.log(err)
        })
    },
    courseSearch() {},
    getDeleted() {
      this.$http
        .post(`/api/courses/manage/deleted`, {
          card_id: this.user.cardID,
          password: this.user.password
        })
        .then(response => {
          this.deletedCourses = response.data
        })
    },
    quitCourses() {
      Dialog.create({
        title: '提示',
        message: '您确定要将已选课程退课吗',
        buttons: [
          '取消',
          {
            label: '退课',
            handler: () => {
              Loading.show()
              this.$http
                .post(`/api/courses/manage/quit`, {
                  card_id: this.user.cardID,
                  password: this.user.password,
                  courses: this.selectedCourses
                })
                .then(response => {
                  this.result = response.data
                  this.getRank()
                })
            }
          }
        ]
      })
    },
    selectCourse() {
      Loading.show()
      this.$http
        .post(`/api/courses/manage/select`, {
          card_id: this.user.cardID,
          password: this.user.password,
          courses: [this.course]
        })
        .then(response => {
          this.result = response.data
          this.courseAddModal = false
          this.getRank()
          this.course = {
            no: '',
            class: ''
          }
        })
    }
  }
}
</script>
