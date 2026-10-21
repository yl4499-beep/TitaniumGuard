# GitHub 留痕与提交说明

## 官方明确要求与建议做法

官方要求把完整、可复现的代码公开到 GitHub，并在 Devpost 提交仓库链接和已部署原型的演示。当前公开评分表没有规定最低 commit 数量、每天提交次数，或必须上传聊天记录。官方工作流程建议按任务保存 commit，这适合记录真实的开发过程。

来源：
- https://github.com/timothyfraser/sixsigmahackathon
- https://github.com/timothyfraser/sixsigmahackathon/blob/main/docs/criteria.md
- https://github.com/timothyfraser/sixsigmahackathon/blob/main/.claude/skills/superagent/SKILL.md

2026-10-21 已公开完整源代码：https://github.com/yl4499-beep/TitaniumGuard。真实提交 00622df 上传了已审核的原型、数据、测试和部署配置；首次 GitHub 自动检查运行 39548738151 已通过。部署运行停在缺少课程 secrets 的检查，尚未上线，也尚未提交 Devpost。历史审计报告保留检查当时的状态。

## 建议保留什么

1. 首次发布完整可运行的版本，可以使用真实的提交说明 `Add reviewed TitaniumGuard prototype`。
2. 后续每次实际修复、文档修改或部署更新，再分别 commit；说明改了什么及为什么改。
3. 保留测试、数据生成代码、数据说明、统计方法来源、AI 使用说明和本次检查报告。
4. 上传源代码目录结构，而不仅上传一个 ZIP。老师应能克隆仓库、照 README 运行。
5. 使用你本人或团队实际的 GitHub 身份，填写真实的组员信息。

现有作品是在 AI 协助下完成的，应按 docs/SOURCES.md 说明 AI 的实际作用。不要补写虚假的早期开发日期或将未完成的团队审核写成已经完成。可从当前完成状态开始真实记录。

## 发布顺序

1. 下载并解压 TitaniumGuard_Project.zip，检查 README 和三个示例。
2. 在你或团队的 GitHub 账户下创建公开仓库，将解压后的 TitaniumGuard 目录作为项目根目录。GitHub Desktop 或命令行都可以。
3. 确认 GitHub 仓库根目录能看到 README.md、app/、data/、demo/、docs/、tests/、SPEC.md 和 CONTRACT.yaml。
4. `.github/workflows/checks.yml` 会在未来的 push/PR 上运行统计/API 测试和部署文件检查。首次运行已通过；后续提交继续查看对应运行结果。
5. 如果采用自动部署，在仓库设置中配置课程发给你的 CONNECT_SERVER 和 CONNECT_API_KEY secrets；部署流程使用课程官方模板。没有这两个配置时，部署工作流会报缺少配置，属于尚未部署。
6. 发布后在未登录浏览器检查应用主页、三个示例、CSV 导入和 `/docs`，把真实地址填写到 README 与 Devpost。
7. 审核 docs/DEVPOST_DRAFT.md，替换团队审核情况和链接占位内容，在截止时间前正式提交。

服务器兼容性、账户权限和匿名访问只能在真实课程服务器上确认。本地全部通过不会自动创建公开仓库、上线应用或提交 Devpost。

## 注意保存数据

应用是课程用的过程分析原型。手工输入的数据保存在当前浏览器标签页内；离开前下载 CSV。真实生产数据应从自己的基线 CSV 开始，避免与示例模拟数据混用。
