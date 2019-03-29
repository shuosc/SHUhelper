# CI/CD说明

我们使用[travis-ci](https://www.travis-ci.org)进行CI/CD。

CI/CD 相关配置见 [.travis.yml](https://github.com/shuopensourcecommunity/SHUhelper/blob/v5/.travis.yml)。

## CI

CI 分为三个阶段:

### Test
目前烂了（TAT），没有启用。

### Build

这阶段会将前端和后端分别构建成 Docker 镜像，并上传到 DockerHub。

### Deploy

这阶段 CI 会 ssh 到开发服务器，并运行[部署脚本](https://github.com/shuopensourcecommunity/SHUhelper/blob/v5/deploy.sh)。

#### 部署方案

我们使用 docker-compose 进行部署。

请见 [docker-compose.yml](https://github.com/shuopensourcecommunity/SHUhelper/blob/v5/docker-compose.yml)。

部署前请注意这里:
```yaml
JWT_SECRET: CHANGE_WHEN_DEPLOY
ADMIN_TOKEN: CHANGE_WHEN_DEPLOY
```
要设置成你想要的JWT密钥和Admin token。
