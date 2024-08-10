# 项目简介
本项目的目标是实现一款可以完全离线使用的数字人直播软件，支持实时语音交互、定制角色、知识库、数字人嘴型同步和制定直播计划。

作者联系方式：

开发者微信号：bigfacewo

策划和美术微信号：leng151213

有任何问题或者合作机会请联系。

# 项目效果

点击此链接查看
https://www.bilibili.com/video/BV1bgYJeCE55/?vd_source=94467fd1f84447c87ac3d86cb2606cff

# 前提和说明
1. 运行环境：必须是支持 cuda 的 nvidia gpu，在之前的实际直播测试中，我们使用的是rtx 4060ti 16g。
2. UE5版本：5.3，仅支持嘴型同步到metahuman制作的人物。
3. 内存大小：64GB及以上。
4. 项目初始运行时，必须能够访问外网，在建立缓存之后可以离线使用。
5. 交互任务的实时性，通常取决于运行程序的机器的性能，影响的部分包括：
   1. 大语言模型响应速度
   2. 语音合成速度

# 功能开发情况和计划

- [x] 支持实时语音交互
- [x] 支持定制角色
- [x] 支持知识库
- [x] 支持嘴型同步
- [x] 支持直播计划脚本
- [ ] 直播计划脚本可视化编辑器
- [ ] 直播计划管理软件
- [ ] All In One, 即将各部分代码封装到一起,形成一个单一软件

# 直播计划脚本功能开发情况

- [x] 支持任务的基础功能，如背景图片、背景音乐等。
- [x] 支持音频任务
- [x] 支持组任务
- [x] 支持互动任务
- [x] 优化长文本的语音生成速度


# 安装部署文档

查看[部署文档](./docs/deploy.md)

# 直播计划脚本文档

查看[直播计划脚本文档](./docs/script.md)

# 配套的UE可执行程序

请转到本项目的 [Release 列表](https://github.com/wukaikailive/digital_people/releases/tag/v1.0.0-beta)下载 ue-digtal-people.7z。

关于UE工程的项目开发文档，后续补充。


# 赞赏

如果我们的工作帮助到了你，欢迎给我们买一杯咖啡：

![zanshang](./docs/zanshang.jpg)