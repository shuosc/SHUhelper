<template lang="pug">
  q-card(:key="evaluation.id" :flat="flat" style="margin:0.8rem 0 0 0 ;" @click="$router.push(`/courses/evaluations/${evaluation.id}`)")
    q-card-title.no-padding 
    q-item(dense)
      //- q-item-side
        q-item-tile(avatar)
          img(:src="`https://static.shuhelper.cn/${evaluation.user.avatar}`")
      q-item-main
        q-item-tile(label) {{evaluation.display_name}}
        q-item-tile(sublabel)  {{[evaluation.created.slice(0,19),'YYYY-MM-DD HH:mm:ss']|moment("from")}}
      //- q-item-side
        q-btn(icon="delete" flat v-if="evaluation.user.cardID == $store.state.user.cardID" @click.stop="deleteEvaluation")
    q-card-separator
    q-card-main 
      p(v-for="paragraph in evaluation.text.split('\\n')")
        | {{ paragraph }}
    //- div.row.flex.xs-gutter(v-if="evaluation.img.length !== 0" style="padding:0.5rem;")
      div.col-4(v-for="(img,key) in evaluation.img" :key="key" @click.stop="")
        img(:src="`${img}-slim75`" @click="showImg(img)"
        style="object-fit: cover;width:100%;height:100%;" 
        alt="lorem")
    q-card-separator
    q-card-actions.justify-end
      q-btn(small :class="{'text-pink':evaluation.liked}" flat @click.stop="onLikeClick(index)")
        q-icon(name="favorite")
        span(style="color:grey;font-size:1rem;")
          | {{evaluation.like.length}}
      q-btn(flat small)
        q-icon(name="comment")
        span(style="color:grey;font-size:1rem;")
          | {{evaluation.comments.length}}
    //- q-card(flat)
      small.text-faded(v-if="evaluation.like.length" style="word-wrap:break-word;")
        span(v-for="(user,ui) in evaluation.like")
          span(v-show="ui!==0") 、
          | {{user.name}}
        span 喜欢了这条动态
      q-list(dense v-if="comments")
        q-item.no-padding(v-for="(comment,index) in evaluation.comments" :key="index")
          q-item-main
            small
              span.text-primary
                | {{comment.user.name}}: 
              | {{ comment.text }}
</template>

<script>
import { parseURL } from '@/../libs/utils.js'
import { Dialog } from 'quasar'
export default {
  props: {
    evaluation: {
      type: Object,
      default() {
        return {
          user: {}
        }
      }
    },
    index: {
      type: Number
    },
    comments: {
      type: Boolean
    },
    flat: {
      type: Boolean
    },
    showDel: {
      type: Boolean,
      default() {
        return false
      }
    }
  },
  filters: {
    urlHost: function(value) {
      return parseURL(value).host
    }
  },
  watch: {
    show: function(val) {
      if (val) {
        this.$store.commit('hideBottomNavgation')
      } else {
        this.$store.commit('showBottomNavgation')
      }
    }
  },
  data() {
    return {
      showModal: false,
      delDialog: false,
      show: false,
      delete: false
    }
  },
  computed: {
    imgs() {
      // console.log(this.evaluation.img)
      let img = this.evaluation.img.map(val => {
        return '//static.shuhelper.cn/' + val
      })
      // console.log(img)
      return img
    }
  },
  methods: {
    showImg(img) {
      this.$q.events.$emit('app:showImg', img)
    },
    onLikeClick(index) {
      let id = this.evaluation.id
      this.$http.get(`/api/evaluations/${id}/like`).then(response => {
        this.evaluation = response.data
      })
    },
    deleteEvaluation() {
      Dialog.create({
        title: '提示',
        message: '确定要删除吗',
        buttons: [
          '取消',
          {
            label: '删除',
            handler: () => {
              this.$http.delete(`/api/evaluations/${this.evaluation.id}`).then(response => {
                this.$emit('delete')
              })
            }
          }
        ]
      })
    }
  }
}
</script>
