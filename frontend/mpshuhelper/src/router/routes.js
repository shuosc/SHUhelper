module.exports = [
  {
    alias: '/',
    path: '/pages/index/index',
    name: 'NewsList',
    config: {
      enablePullDownRefresh: true
    }
  },
  {
    alias: '/lost-n-found',
    path: '/pages/lostNFound/index',
    name: 'lostNFound',
    config: {
      enablePullDownRefresh: true,
      navigationBarTitleText: '失物招领'
    }
  },
  {
    alias: '/lost-n-found/new',
    path: '/pages/lostNFound/new',
    name: 'lostNFoundNew',
    config: {
      navigationBarTitleText: '启事发布'
    }
  },
  {
    alias: '/lost-n-found/post',
    path: '/pages/lostNFound/post',
    name: 'lostNFoundPost',
    config: {
      navigationBarTitleText: '启事详情'
    }
  },
  {
    alias: '/campus',
    path: '/pages/campus/index',
    name: 'campus',
    config: {
      navigationBarTitleText: '校园广场'
    }
  },
  {
    alias: '/campus/new',
    path: '/pages/campus/new',
    name: 'campusNew',
    config: {
      navigationBarTitleText: '发表动态'
    }
  },
  {
    alias: '/school-bus',
    path: '/pages/schoolBus',
    name: 'schoolBus',
    config: {
      navigationBarTitleText: '校车时刻'
    }
  }
]
