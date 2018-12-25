# 代码结构与导读

显而易见的，代码顶层分为三个部分，前端，后端和共享内容。

## 前端

前端是一个典型的 Nuxt 项目，可以参考[官方说明](https://zh.nuxtjs.org/guide/directory-structure)。

## 后端

后端需要关注的结构只有这些：
```bash
.
├── initialData             # 用于初始化的部分数据，可能将在后台管理页面完成后弃用
├── script                  # 工具脚本，现在只有一个普通的开发服务器启动脚本
└── src                     # 主要代码文件夹
    ├── infrastructure      # 基础设施
    │   ├── mongodb.ts
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

每种领域模型中的对象类型都被建模为一个class。

尽量建模成贫血模型。

class中视需要而可能有静态工厂方法：
- `fromJson`：从Json中构造对象
- `fromRawObject`：从Mongo的失血模型构造对应贫血模型。
有序列化为失血模型的方法`serialize`。

使用一个 Repository 来管理所有对象。

目前将 Repository 写为类+静态方法和写为 namespace + 普通函数 基本等效，偏好后一种方法。

Repository 负责从数据库或缓存中查询出符合某种条件的对象，以及将某个对象放到缓存或数据库中。