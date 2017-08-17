<template>
  <div class="schedule">
    <div class="time-ground">
      <div style="height:3.8%;"></div>
      <div v-for="time in timeGround" style="height:7.4%;margin:0" :key="time">
        <span>{{time}}</span>
      </div>
    </div>
    <div class="task-ground">
      <div v-for="(week,index) in weekGround" class="task-list" :key="index">
        <div style="height:3.8%;width:100%;">
          <p style="margin:0;">{{week}}</p>
        </div>
        <div class="taskListSty">
          <div class="task-list-item" v-for="detail in taskDetail[index]" :key="detail" :style="detail.styleObj" @click="showDetail(detail)">
            <div>
              <h5>{{detail.coursename}}</h5>
              <p>{{detail.teachname}}</p>
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
        return ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
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
          '#2B2E4A',
          '#521262',
          '#903749',
          '#53354A',
          '#40514E',
          '#537780'
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
      console.log('showDetail raw')
      this.$emit('showDetail', obj)
    }
  }
}
</script>

<style scoped>
.schedule {
  width: 90%;
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
  height: 100%;
}

.time-ground {
  display: block;
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
}

.time-ground div {
  box-sizing: border-box;
  border-bottom-style: solid;
  border-color: #EAEAEA;
  border-width: 1px;
}

.time-ground div span {
  position: relative;
  left: -20px;
  top: 10px;
}

.task-ground {
  width: 100%;
  height: 100%;
}

.task-list {
  float: left;
  width: 20%;
  box-sizing: border-box;
  border: 1px solid #EAEAEA;
  height: 100%;
}

.task-list p {
  text-align: center;
  font-size: 0.9rem;
}

.task-list-item {
  position: absolute;
  background-color: #577F92;
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

.task-list-item h5 {
  color: #E0E7E9;
}

ul {
  list-style-type: none;
}

.taskListSty {
  position: absolute;
  height: 96.2%;
  width: 20%;
}
</style>
