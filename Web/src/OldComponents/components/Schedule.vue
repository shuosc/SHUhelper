<template>
  <div class="schedule">
    <div class="time-ground">
      <div style="height:3.8%;"></div>
      <div v-for="(time,index)  in timeGround" style="height:7.4%;margin:0" :key="index">
        <div id="time">
          <span style="font-size:0.7rem;color:grey;">{{time.start}}</span><br/>
          <div style="font-size:0.7rem;" id="no"> {{time.no}}</div><br/>
          <span style="font-size:0.7rem;color:grey;">{{time.end}}</span>
        </div>
      </div>
    </div>
    <div class="task-ground">
      <div v-for="(week,index) in weekGround" class="task-list" :key="index">
        <div style="height:3.8%;width:100%;">
          <p style="margin:0;">{{week}}</p>
        </div>
        <div class="taskListSty">
          <div class="task-list-item" v-for="(detail,index) in taskDetail[index]" :key="index" :style="detail.styleObj" @click="showDetail(detail)">
            <div>
              <p id="name">{{detail.coursename}}<br/>({{detail.teachname}})</p>
              <p>@{{detail.place}}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    timeGround: {
      default () {
        return [
          { no: 1, start: '08:00', end: '08:45' },
          { no: 2, start: '08:55', end: '09:40' },
          { no: 3, start: '10:00', end: '10:45' },
          { no: 4, start: '10:55', end: '11:40' },
          { no: 5, start: '12:10', end: '12:55' },
          { no: 6, start: '13:05', end: '13:50' },
          { no: 7, start: '14:10', end: '14:55' },
          { no: 8, start: '15:05', end: '15:50' },
          { no: 9, start: '16:00', end: '16:45' },
          { no: 10, start: '16:55', end: '17:40' },
          { no: 11, start: '18:00', end: '18:45' },
          { no: 12, start: '18:55', end: '19:40' },
          { no: 13, start: '19:50', end: '20:35' }]
      }
    },
    weekGround: {
      type: Array,
      default () {
        return [
          '周一',
          '周二',
          '周三',
          '周四',
          '周五'
        ]
      }
    },
    taskDetail: {
      type: Array,
      default () {
        return []
      }
    },
    color: {
      type: Array,
      default () {
        return [
          '#4DC7C0', '#9BD3C0', '#E2E0BA', '#FFB3B2', ' #FF4A9B', '#BED1FA', '#78FFB5', '#7A00CB'
        ]
      }
    }
  },
  data () {
    return {
      showModal: false
    }
  },
  methods: {
    showDetail (obj) {
      // console.log('showDetail raw')
      this.$emit('showDetail', obj)
    }
  }
}
</script>

<style scoped>
.schedule {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
  padding-left: 2.3rem;
  height: 100%;
}

.time-ground {
  display: block;
  padding-left: 2rem;
  /* margin-left:1.5rem; */
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
}

#time {
  height: 100%;
  position: absolute;
  left: -2rem;
  width: 2rem;
}

.time-ground>div {
  position: relative;
  box-sizing: border-box;
  border-bottom-style: solid;
  border-color: #EAEAEA;
  border-width: 1px;
}

.time-ground>div div#no {
  position: absolute;
  top: 50%;
  text-align: center;
  width: 100%;
  transform: translateY(-50%);
}

.time-ground>div span:first-of-type {
  position: absolute;
  top: 0;
}

.time-ground>div span:last-of-type {
  position: absolute;
  bottom: 0;
}

.task-ground {
  width: 100%;
  /* margin-left:1.5rem; */
  height: 100%;
}

.task-list {
  float: left;
  width: 20%;
  box-sizing: border-box;
  /* border-left: 1px solid #EAEAEA; */
  height: 100%;
}

.task-list p {
  text-align: center;
  font-size: 0.9rem;
}

.task-list-item {
  position: absolute;
  background-color: #577F92;
  /* border-bottom: 1px solid #EAEAEA; */
  width: 100%;
  cursor: pointer;
  text-align: center;
  vertical-align: middle;
}

.task-list-item p {
  padding: 0;
  font-size: 0.8rem;
  color: #EDF2F6;
  margin-bottom: 0.5rem;
}

.task-list-item #name {
  font-size: 0.8rem;
  font-weight: bold;
  /* color: #E0E7E9; */
  color: #E0E7E9;
  margin-bottom: 0.4rem;
  /* padding: 0.1rem; */
  padding-left: 0.3rem;
  padding-right: 0.3rem;
  padding-bottom: 0.5rem;
  padding-top: 1rem;
  text-overflow: ellipsis;
  /* white-space: nowrap; */
  overflow: hidden;
}

ul {
  list-style-type: none;
}

.taskListSty {
  box-sizing: border-box;
  position: relative;
  height: 96.2%;
  width: 100%;
}
</style>
