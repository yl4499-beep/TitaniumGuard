# GitHub 留痕与提交说明

## 当前状态

- 完整源代码已公开：https://github.com/yl4499-beep/TitaniumGuard
- 在线项目已部署：https://connect.systems-apps.com/content/4e02952e-c744-4f24-8791-463876e0bcb5/
- 公开访问已验证：评委无需登录；三个示例的完整 JSON 与已审核结果一致，CSV 下载一致，空输入返回 422。
- GitHub 自动检查已通过：109 项统计/API 测试、20 个 manifest 文件校验和及三组数据镜像检查。
- 公开网站检查工作流已通过：[运行 39697302954](https://github.com/yl4499-beep/TitaniumGuard/actions/runs/39697302954)。
- **尚未提交 Devpost 或 Canvas；真实团队名单和团队审核说明待补充。**

部署通过课程 Posit Connect 的 **Publish → Import from Git** 完成，来源是本仓库 `main` 分支的 `app` 目录。无需另建 API Key。原来的 API Key 部署工作流保留为手动备用方式，不再随 push 运行；不要同时启用两个发布方式。此前缺少 secrets 的失败运行保留为真实历史记录。

详细目标、版本和实际检查输出见 [DEPLOYMENT.md](DEPLOYMENT.md)。

## 代码过程是否必须在 GitHub 完成

公开评分标准要求完整、可复现的代码发布到 GitHub。当前公开要求没有规定最低 commit 数、每日提交次数或上传全部聊天记录。可以在本地或 AI 工具中开发，再把真实修改提交到仓库。

本项目保留了真实的源代码发布、文档更新、部署配置和线上验证提交，以及实际运行的 CI。不要补造早期开发时间或假提交，也不要把未完成的团队审核写成已经完成。

## 接下来提交什么

1. 在 Devpost 中填写实际项目名和团队成员，审核 [DEVPOST_DRAFT.md](DEVPOST_DRAFT.md) 中的文案与 AI 协助说明。
2. 填入上面的 GitHub 链接和在线演示链接。演示视频等字段以实际提交表单为准；当前没有制作或提交视频。
3. 完成 Devpost 正式提交，并保存生成的项目页面链接。
4. [官方 kickoff 幻灯片第 10 页](https://timothyfraser.com/sigma/slides/40_slides_recitation_8.html#10) 还要求在 **Canvas 提交 GitHub 仓库网址和 Devpost 项目链接**。核对实际 Canvas 作业的截止时间和字段。

已公布的 DL 截止时间是 2026 年 10 月 23 日下午 3 点（美国东部时间）。项目上线不等于 Devpost 或 Canvas 已提交。

## 使用与演示

依次展示 Stable process、Mean shift、Low strength margin，解释为什么历史 Cpl 较高时仍然必须优先处理当前过程信号。CSV 是明确标注的模拟数据；900 MPa 和 1.33 是教学示例，不是航空材料标准。

手工输入的数据只保存在当前浏览器标签页内，离开前下载 CSV。真实生产数据应从自己的基线 CSV 开始，避免与示例模拟数据混用。

## 官方来源

- https://six-sigma-hackathon.devpost.com/
- https://github.com/timothyfraser/sixsigmahackathon/blob/main/docs/criteria.md
- https://github.com/timothyfraser/sixsigmahackathon/blob/main/.claude/skills/superagent/SKILL.md
- https://timothyfraser.com/sigma/slides/40_slides_recitation_8.html#10
