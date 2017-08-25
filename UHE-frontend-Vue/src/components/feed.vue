<template>
  <v-card class="mt-3" @click="onFeedClick()">
    <v-container fluid grid-list-lg class="py-0">
      <v-layout row>
        <v-flex xs2 @click.stop>
          <v-card-media :src="`//static.shuhelper.cn/${feed.user.avatar}`"
            height="2.5rem" contain></v-card-media>
        </v-flex>
        <v-flex xs4 @click.stop>
          <div>
            <div style="font-size:1.1rem;" class="teal--text">{{feed.user.name}}</div>
            <div style="font-size:0.5rem;" class="grey--text">
              {{$moment(feed.created,'YYYY-MM-DD hh:mm:ss').fromNow()}}
            </div>
          </div>
        </v-flex>
      </v-layout>
    </v-container>
    <v-container class="pb-0 pt-3 px-3">
      <v-layout row>
        <v-flex xs12>
          {{feed.text}}</v-flex>
      </v-layout>
    </v-container>
    <v-container fluid v-if="feed.img.length !== 0" grid-list-sm
      class="pa-3">
      <v-layout row wrap>
        <v-flex xs4 v-for="(img,key) in feed.img" :key="key"
          @click.stop>
          <img v-img="{group:index}" :src="`//static.shuhelper.cn/${img}-slim75`"
            style="object-fit: cover;" alt="lorem" width="100%"
            height="100%" />
        </v-flex>
      </v-layout>
    </v-container>
    <v-container grid-list-lg v-if="feed.linkURL !== ''"
      style="border-style:solid;border-width:2px;border-color:#eee;"
      class="pa-0 ma-2" @click.stop>
      <v-layout row style="min-height:5rem;">
        <v-flex xs3>
          <v-card-media v-if="feed.linkImg" src="/static/107.jpg"
            style="height:100%;" contain></v-card-media>
          <v-icon x-large v-else style="height:100%;display:flex;"
            class="blue--text text--darken-2">public</v-icon>
        </v-flex>
        <v-flex xs9>
          <p style="font-size:1rem;height:100%;" class="black--text text-xs-left py-2 ma-0"
            @click="this.window.open(feed.linkURL)">{{feed.linkTitle}}</p>
        </v-flex>
      </v-layout>
    </v-container>
    <v-card-actions class="white">
      <!-- <span v-for="people in feed.liked" :key="people.id" style="font-size:0.8rem;">{{people.name}}</span> -->
      <v-spacer></v-spacer>
      <v-btn icon @click.stop="onLikeClick()">
        <v-icon :class="{'pink--text':feed.liked}">favorite</v-icon>{{feed.likecount}}
      </v-btn>
      <v-btn icon>
        <v-icon>comment</v-icon>{{feed.comments}}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>
<script>
export default {
  props: {
    feed: {
      type: Object,
      default () {
        return {
          user: {}
        }
      }
    },
    index: {
      type: Number
    }
  },
  data () {
    return {
      showModal: false
    }
  },
  methods: {
    onFeedClick () {
      this.$emit('onFeedClick', this.index)
    },
    onLikeClick () {
      this.$emit('onLikeClick', this.index)
    }
  }
}
</script>
