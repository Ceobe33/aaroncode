---
date: 2026-09-24
update: 2026-09-24 22:48
title: mcp-communication_with_eachother
author: Rane
tags: [AI, MCP]
category: [ Artificial_Intelligent ]
cover: img/auto_cover/73227f801224.svg
---

# 要为公司建立一个知识库, 以及需要一个扮演项目经理的角色都有哪些实现方法

如果目标是给公司做一套 **「知识库 + AI 项目经理」**，我建议不要把它理解成“部署一个大模型”，而是拆成两个系统：

```text
                    公司 AI PM
                       │
          ┌────────────┴────────────┐
          ↓                         ↓
      公司知识库                  项目系统
          │                         │
   文档 / Wiki / Git          Jira / 飞书 / Git
   规范 / 代码 / 会议         任务 / PR / Milestone
   历史项目 / FAQ             成员 / 进度 / 风险
          │                         │
          └────────────┬────────────┘
                       ↓
                  Agent / LLM
                       ↓
             分析 → 决策辅助 → 执行
```

这里最重要的是：

> **知识库解决“公司知道什么”，AI PM 解决“公司现在应该做什么”。**

两者需要结合，但技术上最好分开建设。

---

## 1. 第一种：RAG 知识库 + 普通 LLM

这是成本最低、最容易落地的方案。

```text
公司文档
 ↓
Embedding
 ↓
Vector DB
 ↓
RAG
 ↓
LLM
 ↓
回答问题
```

例如员工问：

> “我们的角色动画导出流程是什么？”

系统：

```text
问题
 ↓
向量检索
 ↓
找到：
  动画规范.md
  技术方案.pdf
  历史会议记录
 ↓
LLM
 ↓
回答 + 引用来源
```

#### 技术选择

知识源：

* Git
* Markdown
* PDF
* Word
* 飞书/Notion
* Confluence
* 企业网盘
* 邮件
* 会议记录

存储：

* PostgreSQL + pgvector
* Qdrant
* Milvus
* Elasticsearch / OpenSearch

模型：

* 云端 LLM
* 本地 LLM
* 混合

这是最典型的：

> **企业 AI Knowledge Base**

---

## 2. 第二种：知识库 + Agent

比单纯 RAG 更进一步。

```text
             AI
              │
       ┌──────┼──────┐
       ↓      ↓      ↓
    Knowledge Jira   Git
       ↓      ↓      ↓
      RAG    API    API
```

例如：

> “现在这个项目进度怎么样？”

普通 RAG 很难回答，因为“当前进度”并不一定存在于文档里。

Agent 可以：

```text
读取 Jira
 ↓
读取 Git
 ↓
读取 PR
 ↓
读取会议纪要
 ↓
读取项目计划
 ↓
LLM 综合分析
```

最后得到：

```text
项目进度：

客户端：
████████░░ 80%

服务端：
██████░░░░ 60%

当前风险：
1. WebSocket 协议仍存在兼容问题
2. 美术资源交付延期 2 天
3. XXX 模块存在性能风险

建议关注：
XXX 任务需要负责人确认
```

这时候才开始接近：

> **AI 项目经理**

---

## 3. 第三种：真正的 AI PM Agent

如果你真的希望它“扮演项目经理”，核心不是让 Prompt 写：

> “你现在是一个项目经理。”

这基本没什么意义。

真正的 AI PM 应该拥有：

```text
身份
 ↓
项目上下文
 ↓
知识库
 ↓
实时项目数据
 ↓
工具
 ↓
任务状态
 ↓
长期记忆
 ↓
Agent Loop
```

例如：

```text
                    AI PM
                      │
       ┌──────────────┼──────────────┐
       ↓              ↓              ↓
    Knowledge       Project         People
       │              │              │
    RAG/Wiki      Jira/Git        Members
       │              │              │
       └──────────────┼──────────────┘
                      ↓
                   LLM
                      ↓
             Planning / Analysis
                      ↓
             ┌────────┴────────┐
             ↓                 ↓
          建议动作            执行动作
             ↓                 ↓
          人工确认            API
```

---

## 4. AI PM 最重要的是“工具”

例如给它这些 Tool：

```text
get_project()
get_tasks()
get_task()
create_task()
update_task()
assign_task()

get_git_commits()
get_pull_requests()

get_document()
search_knowledge()

get_team_members()
get_member_workload()

send_message()
create_meeting()
```

那么它才真正拥有“手”。

例如你问：

> “为什么这个版本延期？”

Agent：

```text
① 查询 Milestone
② 查询 Jira
③ 查询 Git
④ 查询 PR
⑤ 查询会议纪要
⑥ 查询任务负责人
⑦ 分析依赖关系
```

最后形成：

```text
延期原因

Backend API
 └── 延期 3 天
      └── 原因：协议变更

Client
 └── 等待 Backend API
      └── 阻塞 2 天

QA
 └── 无法开始
      └── 等待 Client
```

这比简单问：

> “总结一下项目情况”

有价值很多。

---

## 5. 第四种：Multi-Agent

项目复杂之后，可以把一个 PM 拆成多个角色。

```text
                 AI PM
                   │
       ┌───────────┼───────────┐
       ↓           ↓           ↓
   技术 Agent    美术 Agent   QA Agent
       │           │           │
      Git         Asset       Test
      Code        Pipeline    Bug
       │           │           │
       └───────────┼───────────┘
                   ↓
                PM Agent
```

例如：

#### 技术 Agent

负责：

```text
代码
架构
性能
编译
Bug
PR
```

#### 美术 Agent

负责：

```text
资源
规范
交付
Spine
模型
材质
```

#### QA Agent

负责：

```text
Bug
测试
回归
版本质量
```

#### PM Agent

只负责：

```text
进度
风险
依赖
资源
优先级
沟通
```

这样比让一个 Agent 什么都做更容易控制。

---

## 6. 第五种：知识图谱

如果公司的知识量非常大，可以进一步做：

```text
                项目
                 │
       ┌─────────┼─────────┐
       ↓         ↓         ↓
      人员       模块       文档
       │         │         │
       ↓         ↓         ↓
      负责      依赖       描述
```

例如：

```text
张三
 ├── 负责 → 登录系统
 ├── 负责 → SDK
 └── 参与 → Project A

Project A
 ├── 使用 → SDK
 ├── 依赖 → Auth Server
 └── 包含 → Login Module
```

这样 AI 可以理解：

> “如果 Auth Server 延期，会影响哪些模块？”

而不是单纯靠关键词搜索。

不过我不建议一开始就上知识图谱。

**RAG + 结构化项目数据**通常已经能解决大量问题。

---

## 7. 第六种：完全本地部署

如果公司非常在意：

```text
源代码
商业机密
客户数据
内部文档
```

可以：

```text
             公司内网
                │
       ┌────────┴────────┐
       ↓                 ↓
    Local LLM        Knowledge DB
       │                 │
       └────────┬────────┘
                ↓
             AI Agent
                │
       ┌────────┼────────┐
       ↓        ↓        ↓
      Git      Jira     Wiki
```

这样数据不出公司。

缺点就是：

**你需要自己承担模型、GPU、推理服务、Agent Runtime、监控和维护。**

---

## 8. 第七种：云端模型 + 公司本地知识库

我反而比较推荐这个作为第一版。

例如：

```text
公司内网

Git / Wiki / Jira
       ↓
   Knowledge API
       ↓
  Permission Layer
       ↓
     Agent
       ↓
   Cloud LLM
```

关键是不要让 LLM 直接访问整个公司数据库。

应该：

```text
User
 ↓
Permission
 ↓
Agent
 ↓
Tool
 ↓
只获取用户有权限的数据
```

否则会产生非常严重的：

> **知识库越强，数据泄漏风险越大**

的问题。

---

## 9. 真正的企业方案应该有权限系统

这一点甚至比模型选择更重要。

比如：

```text
老板
 ├── 所有项目
 ├── 财务
 ├── 人员
 └── 战略

项目经理
 ├── 项目 A
 ├── 项目 B
 └── 项目成员

程序员
 ├── 技术文档
 ├── Git
 └── 自己参与的项目

美术
 ├── 美术规范
 └── 美术项目
```

AI 必须继承：

```text
User Permission
        ↓
Knowledge Retrieval
        ↓
Tool Calling
```

而不是：

```text
LLM
 ↓
整个公司的数据库
```

---

## 10. 我会把系统分成 5 层

如果你是准备**真的给公司搭**，我建议架构从一开始就这么规划：

```text
┌──────────────────────────────┐
│           UI / Chat          │
│     Web / IM / Desktop       │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│          AI PM Agent         │
│                              │
│ Planning / Reasoning / Loop  │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│            Tools             │
│                              │
│ Git / Jira / Wiki / IM / CI  │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│        Knowledge Layer       │
│                              │
│ RAG / Vector DB / Metadata   │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│         Data Sources         │
│                              │
│ Git / Docs / Jira / Meeting  │
└──────────────────────────────┘
```

再加两个横向系统：

```text
Permission / Security
Observability / Audit
```

---

## 11. AI PM 最值得做的功能

不要一开始就追求“像人一样管理项目”。

先做几个**可以量化价值**的功能。

#### ① 每日项目日报

自动生成：

```text
昨天完成：
- XXX
- XXX

今天计划：
- XXX
- XXX

风险：
- XXX

阻塞：
- XXX

需要 PM 决策：
- XXX
```

---

#### ② 自动发现风险

例如：

```text
任务 A
 ↓
依赖 B
 ↓
B 已延期 3 天
 ↓
A 没有更新
```

AI 自动产生：

> A 可能受到 B 延期影响。

这比“聊天机器人”有价值多了。

---

#### ③ 自动追踪承诺

会议里：

> “我周三之前把接口完成。”

系统记录：

```text
Owner: 张三
Task: API
Deadline: 9/25
```

到了 9/25：

```text
Git：没有相关 commit
Jira：任务仍 In Progress
```

AI PM：

> “API 当前仍未完成，可能影响 XXX。”

---

#### ④ 自动会议纪要 → 任务

```text
会议
 ↓
ASR
 ↓
LLM
 ↓
Action Items
 ↓
Jira
```

例如：

```text
张三：
负责修复登录问题
Deadline：周五

李四：
补充接口文档
Deadline：明天
```

然后自动创建任务。

---

#### ⑤ 项目健康度

不是简单给一个“87分”。

而是：

```text
进度
███████░░░

代码
████████░░

Bug
██████░░░░

资源
█████████░

风险
███████░░░
```

并且**每个判断都能追溯到具体数据**。

这比让 LLM 凭感觉评价项目可靠得多。

---

## 12. 最后是一个很重要的设计原则

不要让：

```text
LLM
```

直接成为：

```text
项目经理
```

而应该让它成为：

```text
                    ┌── 数据
                    │
                    ├── 规则
                    │
Project System ─────┤
                    ├── 权限
                    │
                    └── LLM
                           ↓
                       AI PM
```

尤其是涉及：

* 删除任务
* 修改负责人
* 修改 Deadline
* 发布版本
* 给员工发通知
* 改项目计划

最好采用：

```text
AI 建议
  ↓
Human Approval
  ↓
执行
```

而不是让 Agent 自己无限制执行。

---

### 如果是让我从 0 开始给公司建设

我会按这个顺序：

```text
Phase 1
公司文档统一接入
        ↓
RAG 知识库
        ↓
可引用来源的企业 AI

Phase 2
接入 Git / Jira / 飞书
        ↓
AI 查询实时项目状态

Phase 3
AI PM Agent
        ↓
日报 / 周报 / 风险 / 进度

Phase 4
Tool Calling
        ↓
自动创建任务 / 更新任务 / 通知

Phase 5
Agent 自动发现问题
        ↓
主动提醒 PM

Phase 6
Multi-Agent
        ↓
技术 / 美术 / QA / PM

Phase 7
本地模型 / 私有化
        ↓
敏感数据全部内网
```

**不要一开始就做“超级 AI 项目经理”。** 最值得先做的是 **「公司知识库 + Git/Jira/飞书数据接入 + 可引用的 AI PM」**。这三者打通以后，后面的 Agent、自动任务、风险发现才真正有数据基础。

# 一台mac book pro 顶配可以满足需求嘛,有哪些问题呢

可以，但要先明确一个边界：

> **一台顶配 MacBook Pro 足够作为“公司 AI 知识库 + AI PM 的开发/原型服务器”，甚至可以承担小团队的生产环境；但不适合作为整个公司的高并发 AI 推理服务器。**

如果你说的是目前 Apple Silicon 的高内存 MacBook Pro，最高可以做到 **M4 Max + 128GB 统一内存**；Apple 官方规格确认 M4 Max 16 核 CPU / 40 核 GPU 可选 128GB。([苹果支持][1])

### 先给你一个实际判断

假设公司规模：

| 公司规模      | 一台顶配 MBP                         |
| --------- | -------------------------------- |
| 1～5 人开发团队 | ✅ 很够                             |
| 5～20 人    | ✅ 可以做生产环境，但要控制并发                 |
| 20～50 人   | ⚠️ 可以做核心 Agent / 知识库，但不建议所有推理都本地 |
| 50～200 人  | ⚠️ 更适合作为开发/边缘节点                  |
| 200+      | ❌ 不应该把它作为核心 AI 服务                |

关键瓶颈**不是 CPU**。

而是：

```text
统一内存
   ↓
模型大小
   ↓
KV Cache
   ↓
Context
   ↓
并发数
   ↓
推理速度
```

---

## 1. 128GB MacBook Pro 能跑多大的模型？

这是它最有价值的地方。

Apple Silicon 的特点是：

```text
CPU
GPU
NPU
   ↓
共享 Unified Memory
```

所以不像传统 PC：

```text
GPU VRAM = 24GB
系统 RAM = 64GB

模型必须塞进 GPU VRAM
```

Mac 可以：

```text
128GB Unified Memory
        ↓
CPU + GPU 共享
        ↓
模型可以占用非常大的内存
```

而 Ollama 目前已经针对 Apple Silicon 的 unified memory + MLX 做了专门优化，并支持更大的本地模型；官方近期文档也明确建议运行其 Qwen 3.5 35B-A3B coding 模型时使用超过 32GB unified memory。([Ollama][2])

所以：

#### 128GB MBP

比较舒服的范围大概是：

```text
7B / 14B      ████████████████████
30B / 35B     ███████████████████
70B           ██████████████
100B+         ███████
```

具体能不能跑，不只取决于参数量，还取决于：

* quantization
* context length
* KV cache
* MoE / Dense
* runtime
* batch size

甚至现在已经有模型的 Ollama 页面明确给出：某些模型 Q4 权重约需要 **75GB**，128GB unified-memory 机器才是比较实际的最低配置；同时长 context 会继续消耗额外内存。([Ollama][3])

---

## 2. 但“能跑” ≠ “适合公司用”

这是最重要的问题。

例如：

```text
70B Q4
```

假设模型：

```text
≈ 40～50GB
```

看起来：

```text
128GB
- 50GB model
= 78GB
```

好像还有很多。

但实际上还有：

```text
macOS
+
Embedding model
+
RAG database
+
Agent
+
Redis
+
PostgreSQL
+
Vector DB
+
Browser
+
Docker
+
IDE
+
KV Cache
+
Context
```

所以最终可能：

```text
128GB

├── macOS                  10GB
├── LLM                    50GB
├── KV Cache               15GB
├── Embedding               2GB
├── PostgreSQL              2GB
├── Vector DB               4GB
├── Agent                   2GB
├── Docker                  8GB
└── Other                  10GB
                         ─────
                           103GB
```

此时已经没有多少余量。

---

## 3. 最大的问题其实是并发

比如：

```text
一个人问 AI
```

很好。

```text
5 个人同时问
```

开始下降。

```text
20 个人同时问
```

就不是一个 MacBook Pro 最擅长的工作了。

因为：

```text
单用户：

Prompt
 ↓
LLM
 ↓
Response
```

而：

```text
20 users

Prompt ─┐
Prompt ─┤
Prompt ─┤
Prompt ─┤
Prompt ─┤
         ↓
       LLM
         ↓
     GPU/Memory
```

真正消耗资源的是：

> **KV Cache + 并发 decoding + memory bandwidth**

所以公司 AI 服务最容易遇到的不是：

> “模型跑不起来。”

而是：

> **“模型跑得起来，但是大家同时用的时候非常慢。”**

---

## 4. 第二个问题：Apple Silicon 的 GPU 不是 NVIDIA 数据中心 GPU

Mac 的优势是：

> **内存非常大，而且 CPU/GPU 共享。**

但是 NVIDIA 数据中心 GPU 的优势是：

> **GPU memory bandwidth + CUDA ecosystem + 多 GPU scaling。**

比如企业服务器可以：

```text
H100
H200
B200
RTX 6000 Ada
...
```

然后：

```text
GPU × 4
GPU × 8
```

做 inference cluster。

MacBook Pro 基本没有这个扩展路线。

所以：

```text
MacBook Pro
      ↓
单机能力非常强

NVIDIA Server
      ↓
横向扩展能力非常强
```

这是两个完全不同的方向。

---

## 5. 还有一个经常被忽略的问题：Agent 本身

你前面说的是：

> 公司知识库 + AI 项目经理

这里真正需要的计算资源其实是：

```text
RAG
+
LLM
+
Agent
+
Embedding
+
Reranking
+
Database
+
Tool Calling
+
Web
+
Git
+
Jira
+
IM
```

所以我更推荐：

```text
                  MacBook Pro
                       │
             ┌─────────┴─────────┐
             ↓                   ↓
        Knowledge DB         Agent Server
             │                   │
             └─────────┬─────────┘
                       ↓
                    LLM
                       │
                 ┌─────┴─────┐
                 ↓           ↓
             Local LLM    Cloud LLM
```

而不是：

```text
MacBook Pro
     ↓
所有东西全部本地
```

---

## 6. 最合理的是“混合模型”

比如：

#### 简单问题

```text
“公司年假规则是什么？”

        ↓

Local 14B
```

#### 普通代码问题

```text
“这个函数为什么崩？”

        ↓

Local 32B
```

#### AI PM 日常分析

```text
“分析项目 A 当前风险”

        ↓

Local 32B / 70B
```

#### 超复杂任务

```text
“分析整个 UE 项目的架构并给出重构方案”

        ↓

Cloud LLM
```

#### 公司敏感代码

```text
Git
 ↓
Local RAG
 ↓
Local LLM
```

这样你就能同时获得：

```text
隐私
+
低成本
+
本地数据
+
高端云模型能力
```

---

## 7. 还有一个非常实际的问题：MacBook 不适合当服务器

如果你说的是：

> 买一台 MacBook Pro 放办公室，24/7 跑。

我不太推荐。

因为它本质还是：

```text
Laptop
```

而不是：

```text
Server
```

你需要考虑：

* 长时间高负载
* 散热
* 睡眠
* 网络
* 自动重启
* 服务监控
* 磁盘
* 数据备份
* 电源
* 物理安全
* SSD 写入
* 故障恢复

尤其 AI 服务一旦变成公司基础设施：

```text
Mac 死机
 ↓
整个公司 AI PM 挂掉
```

这就不太舒服。

---

## 8. 所以我更推荐一个很有意思的方案

如果预算允许：

```text
              ┌──────────────────┐
              │ MacBook Pro      │
              │ 128GB            │
              │                  │
              │ 开发 / AI / Agent │
              └────────┬─────────┘
                       │
                       ↓
                 Docker / Git
                       │
                       ↓
              ┌──────────────────┐
              │ 公司服务器       │
              │                  │
              │ DB               │
              │ Vector DB        │
              │ Git              │
              │ Knowledge        │
              │ Backup           │
              └────────┬─────────┘
                       │
                       ↓
                 Cloud LLM
```

Mac：

> **AI 工作站**

服务器：

> **公司数据基础设施**

云端：

> **高端推理能力**

这样比“一台 Mac 承包一切”可靠很多。

---

## 9. 如果只有一台机器，我会怎么配？

如果你现在就是：

> “公司给我一台机器，让我从 0 搭 AI PM。”

那么我会优先：

**M4 Max + 128GB Unified Memory + 至少 2TB SSD。**

原因不是 CPU/GPU，而是：

> **128GB 内存是这台机器作为本地 AI 机器最大的价值。**

Apple 官方也提供 64GB / 128GB unified memory 选项，并且 M4 Max 可以配置到 8TB SSD。([苹果支持][1])

如果预算只能：

```text
M4 Max 64GB
```

也完全可以开始。

甚至：

```text
M4 Pro 48GB
```

都足够开发第一版 RAG + Agent。

但如果公司的明确目标是：

> **“我们希望它未来承担本地大模型推理。”**

那我会把钱优先放在：

```text
128GB RAM
```

而不是：

```text
8TB SSD
```

因为 SSD 可以外挂，**Unified Memory 买小了以后无法升级。**

---

## 10. 最关键的判断

如果你的目标是：

#### 「开发公司 AI PM」

**顶配 MBP：完全够。**

#### 「10～20 人公司实际使用 AI PM」

**基本可以，但最好云端/本地混合。**

#### 「几十个人同时用本地 70B」

**不建议。**

#### 「公司级私有 AI 基础设施」

**MacBook 不应该成为最终服务器。**

---

其实如果你准备认真做这个项目，我认为下一步最值得讨论的不是“Mac 能不能跑”，而是：

```text
公司知识库
      ↓
RAG
      ↓
AI PM Agent
      ↓
Git / Jira / 飞书
      ↓
Local LLM + Cloud LLM
```

**我可以直接给你设计一套“单台 128GB MacBook Pro 从 0 搭建公司 AI PM”的完整技术架构，包括模型选型、RAG、向量库、MCP、Agent、权限、Git/Jira/飞书接入，以及哪些东西应该本地、哪些应该调用云端。**

[1]: https://support.apple.com/zh-cn/121553?utm_source=chatgpt.com "MacBook Pro（14 英寸，M4 Pro 或 M4 Max，2024 年） - 技术规格 - 官方 Apple 支持 (中国)"
[2]: https://registry.ollama.com/blog/mlx?utm_source=chatgpt.com "Ollama is now powered by MLX on Apple Silicon in preview · Ollama Blog"
[3]: https://registry.ollama.com/library/laguna-s-2.1%3Af16?utm_source=chatgpt.com "laguna-s-2.1:f16"

> codex 接入 lceda

# 我的理解: 目前大模型在上下文推理能力很强, 训练的数据集够多, 但是连接画板的部分没了解, 也许是训练集不够嘛? 不确定. 帮我再深度剖析一下吧

你的理解**方向是对的，但“训练集不够”只解释了一小部分**。

从你截图里的 PCB 场景看，真正的问题可以拆成：

> **LLM 很擅长“想清楚应该做什么”，但 PCB/EDA 要求它“在一个精确的物理世界里把事情做对”。这两者之间存在巨大的 Grounding（落地/对齐）鸿沟。**

而且这个鸿沟目前正在通过 **MCP + EDA API + 确定性验证工具** 被逐渐补上。2025–2026 年已经有不少 KiCad + MCP 的实践，甚至已经能让 Agent 直接放置元件、连线、布线并调用 ERC/DRC 验证。([KiCad.info Forums][1])

---

## 1. 先看你截图里的事情到底是什么

截图里大概是在做：

```text
自然语言
   ↓
AI
   ↓
理解需求
   ↓
设计电路
   ↓
画原理图
   ↓
连接器件
   ↓
选择封装
   ↓
PCB Layout
   ↓
布线
   ↓
ERC / DRC
   ↓
Gerber
```

注意这里其实包含了**至少 5 种完全不同的能力**。

```text
① 知识
② 推理
③ 视觉理解
④ 对 EDA 软件的操作
⑤ 工程验证
```

现在的大模型主要已经把：

```text
① 知识
② 推理
```

做得非常强。

而真正困难的是：

```text
③ → ④ → ⑤
```

---

## 2. “连接画板”并不是单纯训练数据不够

这是最关键的地方。

假设你告诉 GPT：

> “把 ESP32 的 GPIO1 接到 USB-UART 的 RX。”

对于语言模型来说：

```text
ESP32
GPIO1
UART
RX
```

这些概念它当然知道。

甚至它可以推理：

```text
ESP32 GPIO1
      ↓
UART TX
      ↓
USB-UART RX
```

**但这并不意味着它真的知道你当前 KiCad 工程里的 GPIO1 是哪个 Pin、坐标在哪里、对应哪个 Symbol、PCB 上对应哪个 Pad。**

这就是：

## Grounding

---

## 3. LLM 的世界 vs PCB 的世界

可以把它理解成两个世界：

#### LLM 的世界

```text
文字

ESP32
GPIO1
UART
RX
GND
3.3V
```

这些东西都是：

> **语义**

---

#### PCB 的世界

```text
U1
 ├── Pin 1
 ├── Pin 2
 ├── Pin 3
 ...
 └── Pin 48

Net 17
 ├── U1.3
 ├── R4.1
 └── J2.7

X = 42.5mm
Y = 17.2mm
Layer = F.Cu
Width = 0.2mm
Clearance = 0.15mm
```

这里变成：

> **精确的结构化状态**

所以：

```text
“GPIO1”
```

和：

```text
U1.3
```

是两个完全不同层次的信息。

LLM 需要完成：

```text
自然语言语义
       ↓
EDA 对象
       ↓
具体 Pin
       ↓
具体 Net
       ↓
具体 PCB 坐标
       ↓
实际几何约束
```

这不是单纯多喂一点训练数据就能彻底解决的。

---

## 4. 一个特别好的类比：代码 Agent

你应该会比较容易理解这个。

如果我告诉 AI：

> “把 `foo()` 修改成异步。”

LLM 很容易理解。

但是如果不给它代码：

```cpp
foo();
```

它不知道：

```text
foo() 在哪个文件？
参数是什么？
谁调用它？
线程模型是什么？
生命周期是什么？
```

所以 Codex / Claude Code 之类 Agent 为什么要：

```text
ls
grep
find
read file
LSP
git
compile
test
```

因为：

> **模型不能只靠记忆工作，它必须观察真实环境。**

PCB 完全一样。

---

## 5. 所以 MCP 在这里到底解决什么？

这就是你截图背后非常关键的技术。

假设我们给 LLM：

```text
get_components()
get_pins()
get_nets()
get_board()
get_footprints()

place_component()
connect_pins()
route_trace()

run_erc()
run_drc()
```

那么：

```text
LLM
 ↓
“我需要知道 U1 的 GPIO1”
 ↓
get_pins(U1)
 ↓
真实数据
 ↓
Pin 34 = GPIO1
```

然后：

```text
LLM
 ↓
“把 GPIO1 接到 J2.RX”
 ↓
connect_pins(U1.34, J2.3)
 ↓
KiCad
```

这里发生了一个非常重要的变化：

> **模型不再“猜 PCB”，而是在查询 PCB。**

---

## 6. 这也是为什么 MCP 很适合这种问题

现在已经出现了多个 KiCad MCP 项目。

例如一个 2026 年的 KiCad MCP 实现已经提供：

```text
schematic
PCB
routing
ERC
DRC
BOM
manufacturing
```

等工具。([GitHub][2])

甚至有项目直接把 KiCad API 暴露成 MCP：

```text
LLM
 ↓
MCP
 ↓
KiCad API
 ↓
真实工程
```

而不是：

```text
LLM
 ↓
“模拟”一个 PCB
```

这两种方式可靠性差别巨大。

---

## 7. 但还有一个更深的问题：**空间推理**

这才是 PCB 比代码难很多的地方。

比如：

```text
U1 ───────── R1
 │            │
 │            │
 C1           C2
 │            │
 GND          GND
```

AI 可以理解这个拓扑。

但是实际 PCB 是：

```text
       ┌───────────────┐
       │               │
       │      U1       │
       │               │
       └───────────────┘

             │
             │ 0.2mm
             │
             ▼

     ───────────────────
```

现在要考虑：

```text
几何
距离
角度
层
过孔
阻抗
线宽
间距
EMI
散热
回流路径
```

这已经不是语言推理问题了。

而是：

> **几何优化 + 物理约束 + 多目标优化。**

---

## 8. 这也是为什么“能连通”不等于“设计好了”

你截图中最值得注意的一句话其实就是：

> **“能连通，不等于设计好。”**

这个判断是非常准确的。

例如 AI 完成：

```text
ESP32
 ↓
Regulator
 ↓
Sensor
```

所有 Net 都连通。

DRC 甚至可能也通过。

但依然可能：

```text
❌ 电源噪声
❌ EMI
❌ 高速信号完整性
❌ 地平面回流路径差
❌ 去耦电容位置错误
❌ 热设计差
❌ ADC 噪声
❌ USB 阻抗不对
❌ 天线区域不合理
```

所以：

```text
Connectivity
≠
Electrical correctness
≠
Signal integrity
≠
Physical quality
≠
Production quality
```

这是非常重要的层次。

---

## 9. 于是你会发现：AI 做 PCB 最大的问题其实是 Verification

这也是当前研究里反复出现的问题。

相关研究指出，LLM 用于 EDA 时的一个核心挑战就是生成设计可能包含 bug，而验证本身需要独立的工具和流程；EDA 领域的综述也把 **verification/debugging** 单独作为重要方向。([doi.org][3])

所以真正合理的架构不是：

```text
LLM
 ↓
“我觉得 PCB 没问题”
```

而是：

```text
LLM
 ↓
修改 PCB
 ↓
KiCad
 ↓
ERC
 ↓
DRC
 ↓
SPICE
 ↓
SI/PI
 ↓
Thermal
 ↓
LLM
 ↓
修正
 ↓
再次验证
```

---

## 10. 这就开始变成真正的 Agent Loop

这和我们刚才讨论的 **AI PM** 是完全相同的思想。

```text
       ┌───────────────┐
       │     LLM       │
       │   Reasoning   │
       └───────┬───────┘
               ↓
             Plan
               ↓
       ┌───────────────┐
       │      Tool     │
       │     KiCad     │
       └───────┬───────┘
               ↓
            Execute
               ↓
       ┌───────────────┐
       │   Verification│
       │   ERC / DRC    │
       └───────┬───────┘
               ↓
            Result
               ↓
             LLM
               ↓
           修正方案
               │
               └──────────→
```

这才是：

## Agent

而不是：

## “让 GPT 画 PCB”

---

## 11. 训练数据到底有没有用？

**有，而且非常重要。**

例如训练数据可以让模型学习：

```text
ESP32
 ↓
LDO
 ↓
Decoupling
 ↓
Capacitor
```

以及：

```text
USB
 ↓
ESD
 ↓
Protection
```

甚至：

```text
高速差分线
 ↓
长度匹配
 ↓
阻抗控制
```

这些属于：

> **设计知识 / Design Prior**

但是训练数据解决不了所有问题。

因为当前工程是：

```text
我的 U1
我的 R3
我的 PCB
我的 Layer Stack
我的制造商规则
我的电源
我的元件库
我的尺寸
```

训练数据不可能提前知道。

所以需要：

```text
Training
+
Context
+
Tools
+
Verification
```

---

## 12. 可以把整个系统理解成四层

这是我认为理解这个问题最重要的一张图：

```text
                 AI PCB Agent
                       │
       ┌───────────────┼────────────────┐
       ↓               ↓                ↓
  Knowledge         Context           Tools
       │               │                │
Datasheet          当前工程           KiCad API
Reference          当前板子           ERC
Design Rules       当前需求           DRC
Best Practices     当前状态           SPICE
       │               │                │
       └───────────────┼────────────────┘
                       ↓
                      LLM
                       ↓
                  Planning
                       ↓
                   Execution
                       ↓
                 Verification
                       ↓
                   Feedback
```

四个东西缺一个都很难。

---

## 13. 这也解释了为什么“大模型越来越强”仍然不能直接解决 PCB

假设模型从：

```text
GPT-4
```

变成：

```text
GPT-6
```

它的：

```text
知识 ↑
推理 ↑
代码 ↑
视觉 ↑
```

但是如果：

```text
KiCad API = 0
PCB state = 0
ERC = 0
DRC = 0
SPICE = 0
```

它依然不知道：

> **你电脑里的那个 U3 到底是什么。**

所以这不是单纯：

```text
Model capability
```

问题。

而是：

```text
Model capability
        ×
Environment access
        ×
Structured representation
        ×
Verification
```

---

## 14. 甚至可以进一步解释你截图中的“AI画板”

它真正厉害的地方可能并不是：

> “AI 突然学会 PCB 了。”

而是：

> **有人把 PCB 软件变成了 AI 可以调用的工具。**

这其实和我们前面讨论的公司 AI PM 是完全同一个技术思想。

---

#### AI PM

```text
LLM
 ↓
MCP
 ↓
Jira / Git / 飞书
 ↓
真实项目状态
```

#### AI PCB

```text
LLM
 ↓
MCP
 ↓
KiCad
 ↓
真实 PCB 状态
```

#### AI 编程

```text
LLM
 ↓
Tools
 ↓
Filesystem / Compiler / Git
 ↓
真实代码
```

三者本质上都是：

## **LLM + Context + Tools + Feedback**

---

## 15. 再往深一点：未来真正重要的可能不是“更大的模型”

这个问题其实非常有意思。

如果把 AI PCB 拆开：

```text
           PCB Agent
              │
     ┌────────┼────────┐
     ↓        ↓        ↓
  LLM      EDA Solver  Database
     │        │        │
  Reasoning  Geometry  Parts
             Routing   Datasheet
             DRC       Rules
```

你会发现：

**LLM 并不应该负责所有事情。**

例如：

#### LLM 擅长

```text
需求理解
方案设计
权衡
解释
规划
异常分析
```

#### 专用算法擅长

```text
Routing
Geometry
Optimization
Constraint solving
```

#### EDA 工具擅长

```text
ERC
DRC
Netlist
Gerber
Simulation
```

#### 数据库擅长

```text
Datasheet
Component
Footprint
Price
Availability
```

最终的高级 Agent 很可能不是：

> **“一个超级聪明的模型包办 PCB。”**

而是：

> **“一个超级聪明的调度器，把多个确定性工具组织起来。”**

---

## 16. 这也是为什么你前面问的“本地模型 + Agent”问题在这里突然变得很有意义

如果你真的做这个东西：

```text
Local LLM
    ↓
PCB Agent
    ↓
MCP
    ↓
KiCad
    ↓
ERC / DRC / SPICE
```

你甚至**不一定需要一个特别大的模型**。

因为：

```text
LLM：负责思考
KiCad：负责执行
EDA：负责验证
数据库：负责事实
```

模型只需要做它最擅长的部分。

这叫：

> **把“知识问题”与“执行问题”分离。**

---

### 最后用一句话纠正你原来的理解

你的：

> **“大模型上下文推理很强、训练数据很多，但连接画板可能是训练集不够。”**

可以升级成：

> **“大模型已经具备相当强的通用知识和推理能力，但它缺少对当前 EDA 工程状态的可靠 Grounding，以及对 PCB 设计工具的结构化操作能力和独立验证闭环。因此问题主要不是‘训练数据不够’，而是‘模型 ↔ 工具 ↔ 当前状态 ↔ 验证器’之间没有形成闭环。”**

而现在 2026 年已经明显在往这个方向走：例如 KiCad 的 MCP 项目已经可以让 Agent 读取/修改原理图、布局和布线，并调用 ERC/DRC；有些实现甚至明确把**“模型负责规划、KiCad 负责执行和判定”**作为核心架构。([KiCad.info Forums][1])

另外，最近的 PCB-QA 研究也很能说明问题：研究者发现，把 PCB 转成适合 LLM 的**结构化 JSON 表示**后，模型对元件连接、datasheet 和 SPICE 等问题的回答能力可以明显提升。这说明“**怎么把工程世界表示给模型**”本身就是核心问题，而不只是模型参数量。([arXiv][4])

**所以如果你想继续往下挖，我认为最值得研究的是：为什么“代码 Agent”已经相对成熟，而“PCB Agent / UE Agent / CAD Agent”明显更难——它们其实对应 AI 从“语言世界”进入“物理/状态空间”的一个关键技术跃迁。**

[1]: https://forum.kicad.info/t/kicad-agentic-mcp-an-ai-assistant-that-edits-your-board-through-kicads-own-api-and-lets-kicad-decide-whether-the-result-is-good/71403?utm_source=chatgpt.com "KiCad Agentic MCP — an AI assistant that edits your board through KiCad's own API, and lets KiCad decide whether the result is good - External Plugins - KiCad.info Forums"
[2]: https://github.com/obhox/kicad-mcp?utm_source=chatgpt.com "GitHub - obhox/kicad-mcp: AI-assisted PCB design for KiCAD 10. Native KiCAD plugin — a single Rust binary exposing 171 schematic, layout, routing, design-review, and manufacturing tools to Claude, or the LLM of your choosing · GitHub"
[3]: https://doi.org/10.1145/3736167?utm_source=chatgpt.com "Large Language Models for EDA: Future or Mirage? | ACM Transactions on Design Automation of Electronic Systems"
[4]: https://arxiv.org/abs/2606.23704?utm_source=chatgpt.com "PCB-QA: Evaluating LLMs over the First Printed Circuit Board Design Question-Answer Dataset"

# 助我学习一下mcp

可以。结合你刚才在研究的 **“公司知识库 + AI PM + PCB Agent”**，我建议你不要把 MCP 当成一个“AI 新技术名词”去背，而是直接从**它解决什么问题 → 协议结构 → 写一个 Server → 接到 Agent → 做真实项目**这条线学。

先给你一个最重要的定义：

> **MCP（Model Context Protocol）本质上是一个标准化的“AI ↔ 外部世界”接口协议。**
>
> 它不是大模型，也不是 Agent，也不是 RAG。

官方当前的 MCP SDK 已经把核心能力抽象成 **Tools、Resources、Prompts**，并支持本地 `stdio` 和远程 Streamable HTTP 等传输方式。当前 Python / TypeScript SDK 都已经进入 v2 稳定线。([py.sdk.modelcontextprotocol.io][1])

---

## 1. 先把 MCP 放到整个 AI 架构里

你之前理解的 AI Agent：

```text
                 ┌─────────────┐
                 │     LLM     │
                 └──────┬──────┘
                        ↓
                    Agent Loop
                        ↓
              ┌─────────┼─────────┐
              ↓         ↓         ↓
             Git       Jira      文件
```

传统做法的问题是：

> 每个 AI 应用自己定义一套 Git/Jira/文件工具接口。

于是：

```text
Claude → Git API A
Cursor → Git API B
你的 Agent → Git API C
```

大量重复。

MCP 想解决的是：

```text
                  MCP
                   │
        ┌──────────┼──────────┐
        ↓          ↓          ↓
       Git        Jira       KiCad
        │          │          │
     MCP Server MCP Server MCP Server
```

于是任何支持 MCP 的 Host 都可以连接。

官方对 MCP 的定位就是：用标准协议把 AI 应用连接到**数据和工具所在的系统**。([MCP TypeScript SDK][2])

---

## 2. 你一定要先区分 3 个东西

这是学习 MCP 最容易混淆的地方。

```text
LLM
 │
 ↓
Host
 │
 ├── MCP Client
 │       │
 │       ↓
 │   MCP Server
 │       │
 │       ↓
 │   外部系统
 │
 ↓
User Interface
```

#### Host

AI 应用本身。

例如：

```text
Claude Code
Cursor
VS Code
你自己写的 Agent
```

---

#### MCP Client

Host 里面负责 MCP 协议通信的客户端。

```text
Host
 └── MCP Client
       ↓
    MCP Server
```

---

#### MCP Server

你真正写的东西。

比如：

```text
kicad-mcp
jira-mcp
git-mcp
company-knowledge-mcp
```

它负责把某个系统暴露给 AI。

---

## 3. MCP Server 到底是什么？

假设你有：

```text
battery.py
```

里面：

```python
def get_battery():
    return 87
```

正常情况下，LLM 根本不知道这个函数存在。

MCP Server 做的是：

```text
LLM
 ↓
“有哪些工具？”
 ↓
MCP Server
 ↓
get_battery
```

然后模型看到：

```json
{
  "name": "get_battery",
  "description": "Get current battery percentage",
  "inputSchema": {}
}
```

于是模型就知道：

> 我有一个叫 `get_battery` 的工具可以调用。

---

## 4. MCP 最核心的三个 Primitive

先只记：

```text
Tools
Resources
Prompts
```

官方 SDK 当前也是围绕这三个核心暴露能力。([py.sdk.modelcontextprotocol.io][1])

---

### Tool：让 AI “做事”

这是最重要的。

例如：

```text
create_task()
update_task()
search_git()
run_drc()
place_component()
send_message()
```

特点：

> **Tool 是动作。**

例如你的 AI PM：

```text
AI
 ↓
create_task({
    title: "修复 WebSocket 断线",
    assignee: "张三"
})
 ↓
Jira
```

---

## 5. Resource：让 AI “读取东西”

例如：

```text
company://project/A
company://employee/123
kicad://board/current
git://repo/status
```

Resource 更接近：

> **数据 / 上下文**

例如：

```text
company://project/A
```

返回：

```json
{
  "name": "Project A",
  "status": "development",
  "milestone": "v1.2",
  "deadline": "2026-10-01"
}
```

---

## 6. Prompt：给 Host 提供可复用的提示模板

比如：

```text
/analyze-project
```

背后可以生成：

```text
请分析当前项目：

1. 当前进度
2. 已完成任务
3. 阻塞任务
4. 风险
5. 依赖
6. 建议 PM 关注事项
```

它不是 Tool。

它更接近：

> **标准化 Prompt 模板。**

---

## 7. 用一个你自己的例子理解

我们直接做一个：

## `company-mcp`

假设公司数据库：

```text
company.db
```

里面：

```text
projects
tasks
employees
```

我们给 AI 暴露：

```text
Tools:

get_project()
get_task()
create_task()
update_task()

Resources:

company://project/{id}
company://employee/{id}

Prompts:

analyze_project()
daily_report()
```

整个结构：

```text
                 AI PM
                   │
              MCP Client
                   │
             company-mcp
                   │
       ┌───────────┼───────────┐
       ↓           ↓           ↓
    Projects     Tasks      Employees
                   │
              company.db
```

这已经非常接近你之前说的**公司 AI PM**。

---

## 8. 第一个 MCP Server：不要从复杂项目开始

我建议你用 Python。

因为你现在主要目的是**理解 MCP**，不是研究 SDK 工程。

官方 Python SDK 当前要求 Python 3.10+，安装方式可以直接：

```bash
uv add "mcp[cli]"
```

或者：

```bash
pip install "mcp[cli]"
```

官方也提供 MCP Inspector 来直接测试 Server。([py.sdk.modelcontextprotocol.io][1])

---

## 9. 我们先写一个最小 MCP

`server.py`：

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("company-demo")


@mcp.tool()
def get_project_status(project: str) -> str:
    """Get the current status of a project."""
    return f"{project}: 80% completed"


@mcp.tool()
def create_task(title: str, owner: str) -> str:
    """Create a project task."""
    return f"Created task '{title}' for {owner}"


if __name__ == "__main__":
    mcp.run()
```

这里你只需要理解：

```python
@mcp.tool()
```

意味着：

> **把这个 Python 函数注册成 MCP Tool。**

---

## 10. 这时候发生了什么？

你的函数：

```python
def create_task(title, owner):
```

经过 MCP Server 暴露以后，模型看到的不是 Python：

而是类似：

```text
Tool:
create_task

Description:
Create a project task.

Arguments:
title: string
owner: string
```

然后：

```text
LLM
 ↓
决定调用 create_task
 ↓
MCP Client
 ↓
MCP Server
 ↓
Python function
 ↓
你的数据库/API
```

**这就是 MCP 最核心的价值。**

---

## 11. MCP 不是“让模型直接执行 Python”

这一点非常重要。

错误理解：

```text
LLM
 ↓
执行 Python
```

正确理解：

```text
LLM
 ↓
Tool Call
 ↓
MCP Client
 ↓
MCP Protocol
 ↓
MCP Server
 ↓
你的代码
```

所以 MCP 是一个**协议边界**。

这就非常重要了，因为你可以在这个边界上加入：

```text
权限
日志
参数校验
审计
沙箱
人工确认
```

---

## 12. MCP Inspector

你现在甚至不需要接 ChatGPT / Claude。

官方 MCP SDK 提供 Inspector，可以直接测试 MCP Server。官方 TypeScript 教程也直接使用：

```bash
npx @modelcontextprotocol/inspector ...
```

来连接本地 stdio Server。([MCP TypeScript SDK][3])

Python SDK 官方快速开始同样推荐：

```bash
uv run mcp dev server.py
```

然后用 Inspector 调试。([py.sdk.modelcontextprotocol.io][4])

这非常适合学习。

---

## 13. 为什么 MCP 里面还有 Transport？

你会继续看到：

```text
stdio
Streamable HTTP
SSE
```

先不要深入。

只需要理解：

> **MCP = 协议**
>
> **Transport = 协议消息怎么传输**

---

#### 本地：

```text
Host
 ↓ stdin/stdout
MCP Server
```

叫：

```text
stdio
```

非常适合：

```text
Claude Code
Cursor
VS Code
本地 Agent
```

启动：

```text
Host
 ↓
spawn
 ↓
python server.py
```

---

#### 远程：

```text
Host
 ↓
HTTP
 ↓
MCP Server
```

现在官方 TypeScript SDK 推荐远程场景使用 **Streamable HTTP**；HTTP + SSE 更多是为了兼容旧实现。([MCP TypeScript SDK][5])

---

## 14. 到这里，你应该建立一个非常重要的脑图

```text
                     MCP
                      │
             ┌────────┼────────┐
             ↓        ↓        ↓
           Tools   Resources Prompts
             │        │        │
            做事     数据      模板
             │        │        │
             └────────┼────────┘
                      ↓
                  MCP Server
                      │
               Transport
                /       \
             stdio     HTTP
```

然后：

```text
AI Application
      │
   MCP Client
      │
      ↓
 MCP Server
      │
      ↓
Real World
```

---

## 15. 然后我们进入你真正应该学习的东西

对于你，我建议不要停留在：

> “会写一个 hello world MCP。”

那没什么价值。

直接按照这个路线：

#### Level 1：MCP 基础

```text
Protocol
Host
Client
Server
Tool
Resource
Prompt
Transport
```

↓

#### Level 2：自己写 Server

```text
Python
FastMCP
Tool
Resource
Prompt
Schema
```

↓

#### Level 3：接真实系统

```text
Filesystem
Git
SQLite
REST API
PostgreSQL
```

↓

#### Level 4：Agent

```text
LLM
 ↓
MCP Client
 ↓
Tools
 ↓
Tool Result
 ↓
LLM
```

↓

#### Level 5：企业 AI

```text
                AI PM
                  │
             MCP Client
                  │
     ┌────────────┼─────────────┐
     ↓            ↓             ↓
company-mcp    git-mcp       jira-mcp
     ↓            ↓             ↓
Knowledge       Git           Jira
```

↓

#### Level 6：高级 MCP

再学：

```text
Auth
OAuth
Remote MCP
Sampling
Elicitation
Tasks
Notifications
Subscriptions
Security
```

现在的 MCP 规范已经不只是简单 Tool Calling；当前 SDK 还涉及 sampling、elicitation、tasks、capability negotiation、subscriptions 等机制。([MCP TypeScript SDK][5])

---

## 16. 你甚至可以直接拿你的 ESP32 项目练

这会比写天气 MCP 有意思得多。

例如做：

```text
xiaozhi-mcp
```

暴露：

```text
get_device_status()

get_battery()

get_wifi_status()

get_memory()

get_audio_status()

restart_device()

get_logs()
```

然后：

```text
用户：

“我的设备为什么语音识别变慢了？”

        ↓

LLM
        ↓
MCP
        ↓
get_device_status()
get_memory()
get_wifi_status()
get_audio_status()
get_logs()
        ↓
LLM 分析
```

这就变成了：

> **AI Debug Agent**

而不是 Hello World。

---

## 17. 再进一步就是你刚才看到的 PCB

做：

```text
kicad-mcp
```

例如：

```text
get_components()
get_nets()
get_pins()
get_board_info()

place_component()
connect_net()
route_trace()

run_erc()
run_drc()
```

于是：

```text
用户：

“把 ESP32 的 3.3V 电源接到传感器”

          ↓

LLM
          ↓
get_components()
          ↓
找到 ESP32 / Sensor
          ↓
get_pins()
          ↓
找到 3V3
          ↓
connect_net()
          ↓
KiCad
          ↓
run_erc()
          ↓
结果
          ↓
LLM
```

现在你就真正理解了：

> **为什么 MCP 能让一个普通 LLM 变成 PCB Agent。**

---

## 18. 最后一个很重要的认知

不要把 MCP 理解成：

> **“AI 的 USB 接口。”**

更准确的理解是：

> **MCP 是一种标准化的“能力发现 + 数据访问 + 工具调用”协议，让 AI Host 不需要为每个外部系统设计完全不同的集成方式。**

所以：

```text
LLM
```

是“大脑”。

```text
Agent
```

是“决策循环”。

```text
MCP
```

是“标准化接口”。

```text
MCP Server
```

是“能力适配器”。

```text
Tool
```

是“动作”。

```text
Resource
```

是“可读取的上下文”。

```text
External System
```

才是真正干活的东西。

---

### 我建议我们直接做一个“小型 MCP 课程”

不要一次讲完所有概念。我们可以直接**边做边学**：

```text
第 1 课
MCP 协议到底在解决什么
        ↓
第 2 课
手写第一个 Python MCP Server
        ↓
第 3 课
Tool / Resource / Prompt 的区别
        ↓
第 4 课
MCP Client + LLM
        ↓
第 5 课
做一个 filesystem MCP
        ↓
第 6 课
做 Git MCP
        ↓
第 7 课
做 SQLite / PostgreSQL MCP
        ↓
第 8 课
把多个 MCP 接进 Agent
        ↓
第 9 课
做你的“AI 项目经理”
        ↓
第 10 课
权限 / Sandbox / Security / Remote MCP
```

**第一阶段我建议用 Python，等你理解协议以后，再用 TypeScript 或 C++ 看 MCP 的底层实现。** 这样不会一开始陷入 SDK 细节。官方 Python SDK 的 v2 已经是当前稳定线，且提供完整的 Server / Client / Tool / Resource / Prompt / Transport 实现。([py.sdk.modelcontextprotocol.io][1])

[1]: https://py.sdk.modelcontextprotocol.io/?utm_source=chatgpt.com "MCP Python SDK - MCP Python SDK"
[2]: https://ts.sdk.modelcontextprotocol.io/v2/?utm_source=chatgpt.com "MCP TypeScript SDK"
[3]: https://ts.sdk.modelcontextprotocol.io/v2/get-started/first-server?utm_source=chatgpt.com "Build your first server | MCP TypeScript SDK"
[4]: https://py.sdk.modelcontextprotocol.io/get-started/?utm_source=chatgpt.com "Get started - MCP Python SDK"
[5]: https://ts.sdk.modelcontextprotocol.io/?utm_source=chatgpt.com "MCP TypeScript SDK | MCP TypeScript SDK (v1)"

# 说起来,我也接触了很多类似的适配了

比如语言的lsp, 大模型的mcp, 软件的sdk, 都是这样以减少"中间件"的目的来设计的

对，而且你这个观察其实已经碰到一个很重要的**软件工程抽象规律**了。

不过我会稍微修正一下你的表述：

> **LSP、MCP、SDK 的共同目标，不完全是“减少中间件”，而是“减少点对点适配，让能力通过标准协议/接口被复用”。**

可以把它抽象成：

```text
没有标准：

A ──────→ B
A ──────→ C
A ──────→ D

B ──────→ C
B ──────→ D
C ──────→ D

        ↓

大量 Adapter / Middleware / Glue Code
```

而有标准以后：

```text
             ┌─────────────┐
A ──────────→│             │
B ──────────→│   Standard  │←──────── C
D ──────────→│             │
             └─────────────┘
```

本质上是在把：

> **“双方如何合作”从具体实现中抽出来，变成一个公共契约。**

---

## 1. LSP、MCP、SDK其实处在同一个思想谱系

你可以这样理解：

| 技术            | 解决的问题      | 标准化的东西        |
| ------------- | ---------- | ------------- |
| **LSP**       | 编辑器 ↔ 语言工具 | 语言服务能力        |
| **MCP**       | AI ↔ 外部世界  | AI 使用工具/数据的能力 |
| **SDK**       | 程序 ↔ 软件/平台 | API 调用方式      |
| HTTP          | 程序 ↔ 网络服务  | 网络通信          |
| SQL           | 程序 ↔ 数据库   | 数据查询语言        |
| POSIX         | 程序 ↔ OS    | 操作系统能力        |
| Vulkan/OpenGL | 程序 ↔ GPU   | 图形能力接口        |

例如 LSP：

```text
以前：

VSCode ── C++插件
VSCode ── Rust插件
VSCode ── Go插件
Vim    ── C++插件
Vim    ── Rust插件
...

            ↓

N × M 个适配
```

LSP 出现之后：

```text
              LSP
               │
      ┌────────┼────────┐
      ↓        ↓        ↓
    clangd    rust-analyzer  gopls
      ↑        ↑        ↑
      │        │        │
    VSCode    Neovim    Emacs
```

于是：

> 编辑器不需要理解 C++。
> clangd 也不需要理解 VSCode。

双方只需要理解 **LSP**。

这就是巨大的解耦。

---

## 2. MCP其实就是把这个思想搬到了“AI世界”

你刚刚学习 MCP 时，实际上可以把它和 LSP 放在一起理解。

LSP：

```text
Editor
   ↓
 LSP
   ↓
Language Server
   ↓
Compiler / AST / Index / Project
```

MCP：

```text
AI Host
   ↓
 MCP
   ↓
MCP Server
   ↓
Git / DB / EDA / Browser / Jira / FileSystem
```

甚至可以做一个非常粗暴但很好记的类比：

```text
LSP : AI 之外的“语言工具标准接口”

MCP : AI 之外的“工具/数据标准接口”
```

当然它们协议设计、能力模型并不相同，但**抽象思想非常接近**。

---

## 3. SDK 又稍微不同

这里有一个值得区分的地方。

**SDK 通常不是“标准协议”本身，而是“把接口使用成本封装掉”。**

比如一个服务提供：

```text
POST /users
GET  /users/:id
POST /payment
```

你当然可以自己写：

```cpp
HTTP Request
JSON
Header
Authentication
Retry
Error Handling
...
```

但官方 SDK 给你：

```cpp
client.users.get(id);
client.payment.create(...);
```

所以：

```text
API
 ↓
SDK
 ↓
你的程序
```

SDK 本质上是在减少：

> **重复的胶水代码（Glue Code）**

而 LSP/MCP 更偏向减少：

> **系统之间的耦合和点对点适配。**

所以可以把三者分成：

```text
协议标准
   │
   ├── HTTP
   ├── LSP
   └── MCP

接口抽象
   │
   ├── POSIX
   ├── OpenGL
   └── Vulkan

实现封装
   │
   ├── SDK
   ├── Client Library
   └── Wrapper
```

它们经常组合起来。

---

## 4. 真正厉害的是“组合爆炸”被压平了

这才是你这个观察最有价值的地方。

假设：

```text
10 个 AI Host
10 个工具系统
```

如果每个 Host 都自己适配每个工具：

```text
10 × 10 = 100 个适配
```

如果引入统一协议：

```text
10 个 Host
   ↓
   MCP
   ↓
10 个 Server
```

大约变成：

```text
10 + 10 = 20 个适配
```

当然实际工程中还会有版本、权限、认证、能力差异等复杂问题，但**复杂度增长模型发生了变化**。

这就是标准化最核心的价值之一：

> **把 N×M 问题变成 N+M 问题。**

这其实是软件工程里非常重要的一种能力。

---

## 5. 你之前做的 ESP32 项目里，其实已经到处都是这种东西

例如你的 xiaozhi / ESP32：

```text
ESP32
 │
 ├── FreeRTOS
 │
 ├── ESP-IDF
 │
 ├── LVGL
 │
 ├── WebSocket
 │
 ├── HTTP
 │
 ├── MQTT
 │
 ├── I2S
 │
 ├── ADC
 │
 └── JSON
```

你并没有自己实现：

```text
TCP/IP
HTTP协议
WebSocket协议
JSON解析
任务调度
LCD驱动框架
音频接口
...
```

而是在不断利用**已经标准化/抽象化的接口**。

比如：

```text
你的代码
   ↓
ESP-IDF API
   ↓
FreeRTOS / Driver
   ↓
Hardware
```

这就是一种层次化抽象。

---

## 6. 甚至 C++ 本身也是这个思想

例如：

```cpp
std::vector
std::thread
std::shared_ptr
std::filesystem
```

你不需要知道底层具体：

```text
malloc
pthread
Windows Thread
Mach Thread
Linux syscall
...
```

你只需要依赖：

```cpp
std::thread
```

然后：

```text
        C++ Standard
             ↓
       std::thread
        ↙       ↘
   Windows      Linux
```

所以你现在学习的这些东西，其实可以串起来：

```text
                         抽象 / 标准化
                              │
        ┌─────────────┬───────┼────────────┐
        ↓             ↓       ↓            ↓
       C++           LSP     MCP           HTTP
        ↓             ↓       ↓            ↓
    OS/Runtime      编译器    Tools        Network
        │             │       │            │
        └─────────────┴───────┴────────────┘
                         ↓
                    Application
```

---

## 7. 还有一个更深的规律：标准化“边界”

我觉得这个对你现在理解 AI Agent 特别重要。

一个系统通常不是把所有东西都标准化。

而是：

> **在变化特别剧烈的两个系统之间，建立一个稳定边界。**

例如：

#### LSP

编辑器在变化：

```text
VSCode
Neovim
Emacs
Zed
...
```

语言工具也在变化：

```text
clangd
gopls
rust-analyzer
pyright
...
```

所以中间建立：

```text
             LSP
              │
Editor ←──────┼──────→ Language Server
```

---

#### MCP

AI Host 在变化：

```text
Claude
Cursor
VSCode
自研 Agent
Codex
...
```

外部工具也在变化：

```text
Git
Jira
Postgres
KiCad
Browser
公司内部系统
...
```

所以：

```text
              MCP
               │
AI Host ←──────┼──────→ External System
```

---

## 8. 这也是为什么我之前说 MCP 不等于 Agent

这时候你就能很自然地理解：

```text
LLM
 │
 ↓
Agent Loop
 │
 ↓
MCP
 │
 ↓
Tool
 │
 ↓
External System
```

每一层解决不同的问题：

```text
LLM
= “我应该怎么想？”

Agent
= “我应该下一步做什么？”

MCP
= “我如何标准化地获得/调用能力？”

Tool
= “具体执行什么？”

SDK
= “这个工具具体怎么调用更方便？”

API
= “系统暴露什么能力？”

```

所以 MCP **不是 AI 的大脑**。

它更像：

> **AI 世界的一个“能力总线/标准接口层”。**

---

## 9. 甚至可以继续往前推一步

你现在看到的其实是一个非常大的软件工程趋势：

> **从“实现中心”逐渐走向“接口中心”。**

早期：

```text
我要实现一个功能
↓
我自己写全部代码
```

后来：

```text
我要实现功能
↓
调用 Library
```

再后来：

```text
调用 SDK
↓
API
```

再后来：

```text
不同系统通过标准协议互操作
```

现在 AI Agent 又把这个过程推进了一层：

```text
以前：
程序员决定调用什么 API

现在：
LLM 可以根据上下文
动态发现能力
↓
选择 Tool
↓
调用 Tool
↓
观察结果
↓
继续决策
```

所以 MCP 真正有意思的地方不是：

> “把 Python 函数包装成 Tool。”

而是：

> **让 AI 能够面对一个动态的、可发现的能力空间。**

这也是为什么你前面那个 **“AI 画 PCB”** 的例子会突然变得合理：

```text
LLM
 ↓
MCP
 ↓
KiCad
 ├── get_components()
 ├── get_nets()
 ├── place_component()
 ├── route()
 ├── run_drc()
 └── ...
```

AI 不需要“学会 KiCad 的全部内部实现”。

它只需要：

```text
知道有哪些能力
        ↓
理解能力的输入输出
        ↓
根据当前状态选择能力
        ↓
观察结果
        ↓
继续行动
```

这和你熟悉的 **LSP / SDK / API / C++ interface**，其实是同一条工程思想在不同领域的演化。

**一句话总结：**

> **好的抽象不是减少系统，而是减少系统之间必须互相知道的东西。**

LSP 让编辑器“不需要知道语言实现”；MCP 让 AI“不需要知道工具内部实现”；SDK 让业务代码“不需要知道 API 底层细节”。这就是你现在看到的共同脉络。
