# 代码结构与导读

显而易见的，代码顶层分为三个部分，前端，后端和共享内容。

## 共享内容

为了让前后端可以共享领域模型的结构和行为，以及提供一些和前端/后端使用的特定技术无关的工具代码，我们将这部分代码单独抽取出来放在共享内容中。

其中需要关注的结构有这些：
```
.
├── model               # 领域模型
│   ├── course          # 课程（名字、课程号、教室等信息）
│   │   └── class       # 课（上课时间、上课地点等信息）
│   ├── dateRange       # 日期区间，被semester、holiday等继承
│   ├── semester        # 学期
│   │   └── holiday     # 代表假期
│   │       └── shift   # 调休相关
│   ├── student         # 学生
│   └── teacher         # 教师
└── tools               # 工具
    ├── assert.ts       # 断言库
    ├── clone.ts        # 深拷贝库
    ├── dateTime        # 日期时间处理，填 JS Date、Time不分的坑
    │   ├── date
    │   ├── day
    │   └── time
    └── functools       # 函数式编程工具
        └── maybe.ts    # Maybe monad，参考Haskell Maybe和Scala Option
```

### model设计

每种领域模型中的对象类型都被建模为一个 interface。

将对象的行为都放入对应 Service 中。

这样做的好处有：
1. 便于使用函数式编程范式（使用高阶函数、进行函数组合等）
2. interface 比 class更便于序列化和反序列化

## 前端

前端是一个典型的 Nuxt 项目，可以参考[官方说明](https://zh.nuxtjs.org/guide/directory-structure)。

## 后端

后端需要关注的结构只有这些：
```
.
├── initialData             # 用于初始化的部分数据，可能将在后台管理页面完成后弃用
├── script                  # 工具脚本，现在只有一个普通的开发服务器启动脚本
└── src                     # 主要代码文件夹
    ├── infrastructure      # 基础设施
    │   ├── mongo.ts     
    │   ├── redis.ts
    │   └── request.ts
    ├── main.ts             # 服务器主文件
    ├── middleware          # 服务器中间件，例如auth中间件
    ├── model               # 模型，主要是Repository部分
    └── service   
        ├── crawl           # 从学校网站爬各类信息的爬虫
        └── simulateLogin   # 模拟登录获取cookie
```

#### Repository

对于每种领域模型，我们使用一个 Repository 来管理所有对象。

目前将 Repository 写为类+静态方法和写为 namespace + 普通函数 基本等效，偏好后一种方法。

Repository 负责从数据库或缓存中查询出符合某种条件的对象，以及将某个对象放到缓存或数据库中。

Redis 缓存在 Repository 这一层做。

Repository 中一般来说有这几个函数：

- `cache` 将对象放入缓存
- `getBy...` 用某个字段的值查取对象
- `save` 储存对象（放入缓存和数据库）

#### 关于 id 和 _id

mongo 会自动生成 _id 字段，但部分数据本身就有 id （如从教务系统中爬到的数据）。

我们在数据本身有 id 时，会坚持使用数据本身的 id 而非自动生成的 _id。在数据本身无 id 时才会使用 _id 。
