# 代码结构与导读

显而易见的，代码顶层分为三个部分，前端，后端和共享内容。

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
    ├── model               # 领域模型
    └── service   
        ├── crawl           # 从学校网站爬各类信息的爬虫
        └── simulateLogin   # 模拟登录获取cookie
```

### model设计

每种领域模型中的对象类型都被建模为一个interface。

将对象的行为都放入对应 Service 中。

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
