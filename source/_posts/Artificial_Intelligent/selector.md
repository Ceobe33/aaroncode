---
date: 2026-09-25
update: 2026-09-25 17:03
title: selector
author: Rane
tags: [AI]
category: [ Artificial_Intelligent ]
katex: true
cover: img/auto_cover/9b1050ba917a.svg
---

# 这里提到的分类器是什么,我想学

> 用 0.6B\~2B 的小模型当分类器，我都用两年了

## 这里的“**分类器**”不是特指某个模型，而是指：

> **输入一段数据 → 判断它属于哪个类别 → 输出类别/标签。**

你看到的：

> “用 0.6B～2B 的小模型当分类器，我都用两年了”

通常是在说：**拿一个很小的 LLM / Transformer 模型，不让它负责复杂生成，而只负责做分类判断。**

#### 先用一个最简单的例子理解

假设你做一个 AI Agent，需要判断用户说的话属于什么类型：

```text
用户输入：
"帮我查一下明天上海天气"

        ↓

     分类器
        ↓

   WEATHER_QUERY
```

再比如：

```text
"帮我把这句话翻译成日文"
        ↓
   TRANSLATION

"打开客厅的灯"
        ↓
   HOME_CONTROL

"你觉得 C++ shared_ptr 是怎么实现的？"
        ↓
   TECHNICAL_QA
```

这就是**文本分类（Text Classification）**。

---

### 为什么 0.6B～2B 模型特别适合做这个？

因为分类任务其实比“生成答案”简单很多。

比如一个 Agent：

```text
                 用户输入
                    │
                    ▼
             ┌─────────────┐
             │  0.6B 模型   │
             │   分类器     │
             └──────┬──────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
     天气查询     设备控制      普通知识
        │           │           │
        ▼           ▼           ▼
    Weather API   ESP32      大模型
```

分类器只需要回答：

```json
{
  "intent": "device_control"
}
```

而不是自己生成一大段回答。

所以模型可以非常小，速度也非常快。

---

## 你真正应该学的是这一套

如果你想学这个，我建议不要一上来学“0.6B 模型”。

先把**机器学习里的分类问题**搞明白：

```text
分类器
  ↓
特征
  ↓
模型
  ↓
训练
  ↓
损失函数
  ↓
梯度下降
  ↓
推理
```

最简单的分类器甚至不需要神经网络。

例如：

```text
输入：
年龄 = 25
收入 = 8000
是否有房 = 1

        ↓

   Logistic Regression

        ↓

贷款违约概率 = 0.13
```

然后：

```text
0.13 < 0.5
       ↓
   不违约
```

这就是分类器。

---

## 再往前一步：神经网络分类器

比如你有：

```text
"这个产品很好用"
"太垃圾了"
"一般般吧"
```

希望分类：

```text
POSITIVE
NEGATIVE
NEUTRAL
```

神经网络可以变成：

```text
文本
 ↓
Tokenizer
 ↓
Embedding
 ↓
Transformer
 ↓
Linear
 ↓
Softmax
 ↓
[0.92, 0.03, 0.05]
```

对应：

```text
POSITIVE = 0.92
NEGATIVE = 0.03
NEUTRAL  = 0.05
```

于是分类结果：

```text
POSITIVE
```

这里最后那个：

```text
Linear → Softmax
```

其实就是非常典型的**分类头（classification head）**。

---

## 那 0.6B～2B LLM 又是什么玩法？

这就比较有意思了。

传统分类：

```text
文本
 ↓
Encoder
 ↓
Classification Head
 ↓
类别
```

而 LLM 分类可以直接：

```text
文本
 ↓
小 LLM
 ↓
JSON
```

例如：

```text
System:

你是一个意图分类器。

类别：
1. weather
2. device
3. coding
4. chat

只输出类别名称。
```

输入：

```text
"ESP32 的电池电量怎么读取？"
```

输出：

```text
device
```

这就是你看到的：

> **“用 0.6B～2B 的小模型当分类器”**

---

## 为什么这东西对你尤其有意思

结合你现在做的 **ESP32 + xiaozhi + AI Agent**，分类器其实非常实用。

比如你现在有：

```text
用户说话
   ↓
ASR
   ↓
LLM
   ↓
执行
```

可以改成：

```text
             ASR
              │
              ▼
       ┌──────────────┐
       │   小模型      │
       │ Intent分类器  │
       └──────┬───────┘
              │
       ┌──────┼──────────┐
       ▼      ▼          ▼
     查询    控制       闲聊
       │      │          │
       ▼      ▼          ▼
    API      Tool       大模型
```

例如：

```text
"现在几点了？"
        ↓
TIME_QUERY

"我的设备还有多少电？"
        ↓
BATTERY_QUERY

"把屏幕亮度调低"
        ↓
DEVICE_CONTROL

"给我讲讲 shared_ptr"
        ↓
GENERAL_QA
```

其中：

```text
BATTERY_QUERY
DEVICE_CONTROL
TIME_QUERY
```

这些甚至**完全没必要让大模型参与**。

---

### 如果你想系统学，我建议这条路线

你本身正在补 C++ / 底层，所以不建议直接从 Transformers 源码啃。

#### Level 1：先理解分类

自己用 Python 实现：

```text
Logistic Regression
        ↓
Softmax
        ↓
Cross Entropy
        ↓
Gradient Descent
```

目标：

```text
输入二维数据
      ↓
分类
      ↓
自己实现训练
```

---

#### Level 2：神经网络分类器

自己实现：

```text
X
 ↓
Linear
 ↓
ReLU
 ↓
Linear
 ↓
Softmax
 ↓
Cross Entropy
```

然后理解：

```text
forward
backward
gradient
optimizer
```

这个阶段你会真正理解“模型训练”是什么。

---

#### Level 3：文本分类

学习：

```text
Tokenizer
Embedding
Transformer
Classification Head
```

做一个：

```text
用户输入
 ↓
意图分类
 ↓
weather / coding / device / chat
```

---

#### Level 4：小模型 LLM 分类器

再进入：

```text
0.5B
0.6B
1B
1.5B
2B
```

理解：

```text
instruction tuning
SFT
LoRA
QLoRA
quantization
```

最后自己训练一个：

```text
0.5B～1B
Intent Classifier
```

---

#### Level 5：把它塞进你的 ESP32 Agent

最终架构可以变成：

```text
              Microphone
                  │
                  ▼
                 ASR
                  │
                  ▼
          ┌───────────────┐
          │ Small Model   │
          │  Intent       │
          │  Classifier   │
          └───────┬───────┘
                  │
       ┌──────────┼───────────┐
       ▼          ▼           ▼
    Battery     Device      General
     Query      Control       QA
       │          │           │
       ▼          ▼           ▼
     Local      Local       Cloud
```

这其实已经开始接近**真正的 Agent 系统设计**了。

而且有一个非常关键的思想：

> **不要让“大模型”解决所有问题。先用便宜、快速、确定性更高的小模型/规则把问题分流。**

这也是你看到那句话值得学习的地方。

如果你愿意，我建议下一步直接从 **“手写一个最小文本分类器”** 开始，不用 PyTorch 黑盒：我可以带你从 `x → Linear → Softmax → CrossEntropy → Backprop` 一步一步写出来。

# 帮我手写一个最小文本分类器

可以。我们直接**手写一个最小可训练文本分类器**，不使用 PyTorch / Transformers，把核心链路全部暴露出来。

目标非常小：

```text
"打开客厅灯"       → device
"还有多少电"       → battery
"今天天气怎么样"   → weather
```

最终你会亲手实现：

```text
文本
 ↓
分词
 ↓
Bag-of-Words 向量
 ↓
Linear
 ↓
Softmax
 ↓
预测类别
 ↓
Cross Entropy
 ↓
反向传播
 ↓
更新权重
```

这比一上来搞 0.6B LLM 更适合真正理解“分类器”。

---

## 1. 先做最小版本
可以。我们就在你上一版 **Embedding + Mean Pooling** 上继续升级。

核心目标不是先做一个能用的 Transformer，而是**手写出 Self-Attention 最小数学闭环**：

```text
Token
 ↓
Embedding
 ↓
Q / K / V
 ↓
QKᵀ / √d
 ↓
Softmax
 ↓
Attention × V
 ↓
新的 Token 表示
```

你理解这套以后，Transformer 的核心就已经打开了。

---

# 1. 先理解：Attention 到底解决什么问题？

你上一版是：

```text
"打开客厅灯"

Embedding
   ↓
E["打"]
E["开"]
E["客"]
E["厅"]
E["灯"]
   ↓
Mean
   ↓
一个句向量
```

问题是：

```text
"打开灯"
```

和：

```text
"灯打开"
```

经过 Mean 后，本质上是同一堆向量相加。

**词序和 token 之间的关系丢失了。**

Self-Attention 的思路是：

> 每个 token 都问一遍：**“我现在应该关注其他哪些 token？”**

例如：

```text
打开 客厅 灯
 │    │    │
 └────┼────┘
      │
      ▼
   Attention
```

“打开”可能更关注“灯”。

“客厅”也可能更关注“灯”。

于是每个 token 都会得到一个**结合上下文后的新表示**。

---

# 2. 最小 Self-Attention

先完全抛开训练。

假设有 3 个 token：

```text
X =
[
    [1, 0],
    [0, 1],
    [1, 1]
]
```

也就是：

```text
token1 = [1, 0]
token2 = [0, 1]
token3 = [1, 1]
```

我们希望得到：

```text
输出 =
[
    新 token1,
    新 token2,
    新 token3
]
```

---

# 3. Q / K / V 是什么？

这是第一次学 Attention 最容易混乱的地方。

不要把它想得太复杂。

可以暂时理解成：

```text
Q = Query
K = Key
V = Value
```

每个 token 都生成三份东西：

```text
                ┌── Q：我想找什么？
Token ──────────┼── K：我有什么特征？
                └── V：如果别人关注我，我提供什么信息？
```

数学上：

$$
Q=XW_Q
$$

$$
K=XW_K
$$

$$
V=XW_V
$$

其中：

```text
WQ
WK
WV
```

都是**可训练参数**。

---

# 4. 第一版我们甚至可以不训练 WQ/WK/WV

为了理解原理，先直接：

```python
Q = X
K = X
V = X
```

也就是：

```text
WQ = I
WK = I
WV = I
```

这样可以把 Attention 的核心完全暴露出来。

---

# 5. 第一步：Q × Kᵀ

假设：

```text
Q =
[
 [1, 0],
 [0, 1],
 [1, 1]
]
```

K 一样。

计算：

$$
S=QK^T
$$

代码：

```python
def matmul(A, B):
    rows = len(A)
    cols = len(B[0])
    inner = len(B)

    result = [
        [0.0] * cols
        for _ in range(rows)
    ]

    for i in range(rows):
        for j in range(cols):
            for k in range(inner):
                result[i][j] += A[i][k] * B[k][j]

    return result


def transpose(A):
    return [
        list(row)
        for row in zip(*A)
    ]
```

然后：

```python
scores = matmul(Q, transpose(K))
```

得到：

```text
[
 [1, 0, 1],
 [0, 1, 1],
 [1, 1, 2]
]
```

---

# 6. 这个矩阵是什么意思？

这是 Attention 最关键的一步。

```text
        K1   K2   K3

Q1      1    0    1
Q2      0    1    1
Q3      1    1    2
```

例如第一行：

```text
[1, 0, 1]
```

表示：

```text
Q1 和 K1 → 相似度 1
Q1 和 K2 → 相似度 0
Q1 和 K3 → 相似度 1
```

所以：

> **QKᵀ 本质上是在计算 token 与 token 之间的相关程度。**

---

# 7. 为什么除以 √d？

Transformer 不直接使用：

```text
QKᵀ
```

而是：

$$
S=\frac{QK^T}{\sqrt{d_k}}
$$

这里：

```text
d_k = Key 的维度
```

如果：

```text
d_k = 64
```

就除以：

```text
√64 = 8
```

代码：

```python
import math

def scale_scores(scores, dim):

    scale = math.sqrt(dim)

    return [
        [
            value / scale
            for value in row
        ]
        for row in scores
    ]
```

为什么？

因为维度很大时：

```text
Q · K
```

的数值可能越来越大。

然后进入 Softmax：

```text
exp(很大的数字)
```

容易导致：

```text
softmax
↓
几乎 one-hot
```

梯度也容易变得不好。

所以：

```text
QKᵀ / √d
```

是一种数值尺度控制。

---

# 8. Softmax

现在：

```text
scores
```

变成：

```text
[
 [0.707, 0, 0.707],
 [0, 0.707, 0.707],
 [0.707, 0.707, 1.414]
]
```

接下来每一行做 Softmax。

注意：

> **每一行单独 Softmax。**

代码：

```python
def softmax_row(row):

    max_value = max(row)

    exps = [
        math.exp(x - max_value)
        for x in row
    ]

    total = sum(exps)

    return [
        x / total
        for x in exps
    ]


def softmax_matrix(matrix):

    return [
        softmax_row(row)
        for row in matrix
    ]
```

得到类似：

```text
[
 [0.401, 0.198, 0.401],
 [0.198, 0.401, 0.401],
 [0.248, 0.248, 0.503]
]
```

这就是：

> **Attention Weights**

---

# 9. 这个矩阵才是 Self-Attention 的灵魂

假设：

```text
A =
[
 [0.4, 0.2, 0.4],
 [0.2, 0.4, 0.4],
 [0.25,0.25,0.5]
]
```

可以把它看成：

```text
             我应该关注谁？

          T1     T2     T3
T1       0.4    0.2    0.4
T2       0.2    0.4    0.4
T3       0.25   0.25   0.5
```

比如：

```text
T1
```

最终会：

```text
40% × V1
20% × V2
40% × V3
```

所以：

> **Attention = 根据相关性，对其他 token 的信息进行加权平均。**

这句话非常重要。

---

# 10. 最后一步：Attention × V

数学公式：

$$
Output = Attention \cdot V
$$

代码：

```python
output = matmul(attention, V)
```

完整 Attention：

```python
def self_attention(X):

    Q = X
    K = X
    V = X

    # QK^T

    scores = matmul(
        Q,
        transpose(K)
    )

    # scaling

    scores = scale_scores(
        scores,
        len(K[0])
    )

    # softmax

    attention = softmax_matrix(
        scores
    )

    # weighted sum

    output = matmul(
        attention,
        V
    )

    return output, attention
```

这就是一个**真正的 Self-Attention**。

没有 PyTorch。

没有 Transformer 库。

没有黑盒。

---

# 11. 用一个实际例子

假设：

```python
X = [
    [1.0, 0.0],
    [0.0, 1.0],
    [1.0, 1.0],
]
```

运行：

```python
output, attention = self_attention(X)

print("attention:")
for row in attention:
    print(row)

print("output:")
for row in output:
    print(row)
```

你会看到类似：

```text
attention:
[0.401, 0.198, 0.401]
[0.198, 0.401, 0.401]
[0.248, 0.248, 0.503]
```

然后：

```text
output:
[0.802, 0.599]
[0.599, 0.802]
[0.751, 0.751]
```

注意一个非常关键的变化：

输入：

```text
T1 = [1, 0]
```

输出：

```text
T1 = [0.802, 0.599]
```

它已经不再只是自己的信息。

而是：

```text
T1
 ↓
关注 T1 / T2 / T3
 ↓
混合其他 token 信息
 ↓
新的 T1
```

这就是 Context。

---

# 12. 为什么叫 Self-Attention？

因为：

```text
Q
K
V
```

全部来自：

```text
同一个 X
```

即：

```text
X
├──→ Q
├──→ K
└──→ V
```

所以叫：

> **Self-Attention**

如果 Q 来自一个序列，而 K/V 来自另一个序列，就是：

> Cross-Attention

---

# 13. 现在把 Q/K/V 变成真正可训练的

刚才为了学习，我们用了：

```python
Q = X
K = X
V = X
```

真正 Transformer 是：

```text
X
 │
 ├── Linear(WQ) → Q
 │
 ├── Linear(WK) → K
 │
 └── Linear(WV) → V
```

也就是：

$$
Q=XW_Q
$$

$$
K=XW_K
$$

$$
V=XW_V
$$

我们手写一个 Linear：

```python
def linear(X, W):

    return matmul(X, W)
```

假设：

```python
X = [
    [0.2, 0.5, 0.1, 0.7],
    [0.8, 0.1, 0.3, 0.2],
    [0.4, 0.6, 0.9, 0.1],
]
```

然后：

```python
WQ = random_matrix(4, 4)
WK = random_matrix(4, 4)
WV = random_matrix(4, 4)

Q = linear(X, WQ)
K = linear(X, WK)
V = linear(X, WV)
```

---

# 14. 完整版本

现在可以把真正的结构写出来：

```python
import math
import random


def matmul(A, B):

    rows = len(A)
    cols = len(B[0])
    inner = len(B)

    result = [
        [0.0] * cols
        for _ in range(rows)
    ]

    for i in range(rows):

        for j in range(cols):

            for k in range(inner):

                result[i][j] += (
                    A[i][k] * B[k][j]
                )

    return result


def transpose(A):

    return [
        list(row)
        for row in zip(*A)
    ]


def random_matrix(rows, cols):

    return [
        [
            random.uniform(-0.1, 0.1)
            for _ in range(cols)
        ]
        for _ in range(rows)
    ]


def softmax_row(row):

    maximum = max(row)

    exps = [
        math.exp(x - maximum)
        for x in row
    ]

    total = sum(exps)

    return [
        x / total
        for x in exps
    ]


def softmax_matrix(matrix):

    return [
        softmax_row(row)
        for row in matrix
    ]


def self_attention(X):

    dim = len(X[0])

    # Learnable parameters

    WQ = random_matrix(dim, dim)
    WK = random_matrix(dim, dim)
    WV = random_matrix(dim, dim)

    # Q K V

    Q = matmul(X, WQ)

    K = matmul(X, WK)

    V = matmul(X, WV)

    # QK^T

    scores = matmul(
        Q,
        transpose(K)
    )

    # Scale

    scale = math.sqrt(dim)

    for i in range(len(scores)):

        for j in range(len(scores[i])):

            scores[i][j] /= scale

    # Softmax

    attention = softmax_matrix(
        scores
    )

    # Attention × V

    output = matmul(
        attention,
        V
    )

    return output, attention
```

这里有一个**重要问题**：

```python
WQ = random_matrix(...)
```

如果放在：

```python
self_attention()
```

里面，那么每次调用都会重新随机生成参数。

**真正训练时绝对不能这么做。**

应该：

```python
WQ
WK
WV
```

作为模型参数长期保存。

所以正式模型应该类似：

```python
class SelfAttention:

    def __init__(self, dim):

        self.WQ = random_matrix(dim, dim)
        self.WK = random_matrix(dim, dim)
        self.WV = random_matrix(dim, dim)

    def forward(self, X):

        Q = matmul(X, self.WQ)
        K = matmul(X, self.WK)
        V = matmul(X, self.WV)

        scores = matmul(
            Q,
            transpose(K)
        )

        scale = math.sqrt(len(K[0]))

        for i in range(len(scores)):
            for j in range(len(scores[i])):
                scores[i][j] /= scale

        attention = softmax_matrix(scores)

        output = matmul(
            attention,
            V
        )

        return output, attention
```

---

# 15. 到这里，你应该看到一个很漂亮的演化

我们之前：

```text
中文
 ↓
Token
 ↓
Embedding
 ↓
Mean
 ↓
Linear
 ↓
Softmax
```

现在：

```text
中文
 ↓
Token
 ↓
Embedding
 ↓
┌─────────────────────┐
│   Self-Attention     │
│                     │
│ X → Q               │
│ X → K               │
│ X → V               │
│                     │
│ QKᵀ                 │
│ ↓                   │
│ /√d                 │
│ ↓                   │
│ Softmax             │
│ ↓                   │
│ × V                 │
└─────────┬───────────┘
          ↓
       Context
          ↓
       Linear
          ↓
       Softmax
```

---

# 16. 还有一个你现在必须注意的问题：它仍然不知道顺序

即使有 Self-Attention：

```text
"打开灯"
```

和：

```text
"灯打开"
```

如果输入 Embedding 完全一样，只是交换位置，那么 Attention 本身仍然无法知道：

```text
第一个 token
```

和：

```text
第二个 token
```

的区别。

所以 Transformer 还需要：

```text
Positional Encoding
```

也就是：

```text
Embedding
+
Position
↓
Transformer
```

例如：

```text
打开 灯
 ↓   ↓
E0  E1

灯 打开
 ↓   ↓
E0  E1
```

通过位置编码以后：

```text
打开 = token embedding + position 0
灯   = token embedding + position 1
```

和：

```text
灯   = token embedding + position 0
打开 = token embedding + position 1
```

就不一样了。

---

# 17. 所以 Transformer 的最小完整结构

我们现在已经走到这里：

```text
              Token IDs
                  │
                  ▼
              Embedding
                  │
                  ▼
         + Positional Encoding
                  │
                  ▼
            ┌───────────┐
            │   Q = XWQ │
            │   K = XWK │
            │   V = XWV │
            └─────┬─────┘
                  │
                  ▼
               QKᵀ / √d
                  │
                  ▼
                Softmax
                  │
                  ▼
                 × V
                  │
                  ▼
           Attention Output
                  │
                  ▼
            Feed Forward
                  │
                  ▼
             Classifier
                  │
                  ▼
              Category
```

**下一步最值得手写的是 `Positional Encoding + Multi-Head Attention + 一个最小 Transformer Block`。**

尤其是 Multi-Head 不需要把它想得很神秘：本质上就是**把 embedding 维度切成几个头，每个头独立做一次 Q/K/V Attention，然后拼回来**。这一步做完，你就已经从“手写 NLP 分类器”真正走进 Transformer 内部了。

为了让代码足够透明，我们先不用中文分词库，直接把输入设计成英文 token：

```text
"turn on light"
"turn off light"
"battery level"
"battery remaining"
"weather today"
"weather tomorrow"
```

类别：

```text
device
battery
weather
```

训练数据：

```python
samples = [
    ("turn on light", "device"),
    ("turn off light", "device"),
    ("open door", "device"),

    ("battery level", "battery"),
    ("battery remaining", "battery"),
    ("how much battery", "battery"),

    ("weather today", "weather"),
    ("weather tomorrow", "weather"),
    ("is it raining", "weather"),
]
```

---

## 2. 第一步：文本 → 数字

神经网络不能直接理解：

```text
"battery level"
```

所以首先建立 vocabulary：

```text
battery
level
turn
on
light
...
```

假设最终：

```text
battery → 0
level   → 1
turn    → 2
on      → 3
light   → 4
...
```

那么：

```text
"battery level"
```

变成：

```text
[1, 0, 0, 0, ...]
```

这叫 **Bag-of-Words（词袋模型）**。

比如 vocabulary：

```text
["battery", "light", "weather", "turn", "level"]
```

那么：

```text
"battery level"
```

就是：

```text
[1, 0, 0, 0, 1]
```

注意：

> 这里完全没有理解语义，只是在统计“哪些词出现了”。

这正好适合作为我们的第一版。

---

## 3. 分类器本体其实只有一层

假设输入：

```text
x = [1, 0, 0, 0, 1]
```

我们建立：

```text
x
 │
 ▼
┌──────────────┐
│ Linear       │
│ y = Wx + b   │
└──────┬───────┘
       │
       ▼
    Softmax
       │
       ▼
[0.02, 0.95, 0.03]
```

对应：

```text
device  = 0.02
battery = 0.95
weather = 0.03
```

所以：

```text
battery
```

---

## 4. 直接手写

新建：

```text
classifier.py
```

代码：

```python
import math
import random


## -------------------------
## 训练数据
## -------------------------

samples = [
    ("turn on light", "device"),
    ("turn off light", "device"),
    ("open door", "device"),

    ("battery level", "battery"),
    ("battery remaining", "battery"),
    ("how much battery", "battery"),

    ("weather today", "weather"),
    ("weather tomorrow", "weather"),
    ("is it raining", "weather"),
]


## -------------------------
## 建立 vocabulary
## -------------------------

vocab = {}

for text, _ in samples:
    for word in text.split():
        if word not in vocab:
            vocab[word] = len(vocab)

print("vocab:", vocab)


## -------------------------
## labels
## -------------------------

labels = {
    "device": 0,
    "battery": 1,
    "weather": 2,
}


## -------------------------
## Bag-of-Words
## -------------------------

def encode(text):
    x = [0.0] * len(vocab)

    for word in text.split():
        if word in vocab:
            x[vocab[word]] += 1.0

    return x
```

现在：

```python
print(encode("battery level"))
```

可能得到：

```text
[1.0, 1.0, 0.0, ...]
```

---

## 5. Softmax

这是分类器非常核心的一步。

假设 Linear 输出：

```text
[2.0, 4.0, 1.0]
```

我们需要把它变成概率。

公式：

$$
softmax(x_i)=\frac{e^{x_i}}{\sum_j e^{x_j}}
$$

代码：

```python
def softmax(xs):
    max_x = max(xs)

    exps = [
        math.exp(x - max_x)
        for x in xs
    ]

    total = sum(exps)

    return [
        x / total
        for x in exps
    ]
```

这里：

```python
max_x = max(xs)
```

不是数学上必须的，而是为了防止：

```python
math.exp(1000)
```

溢出。

这是实际机器学习代码里非常常见的数值稳定技巧。

---

## 6. Linear 层

我们的模型：

```text
y = Wx + b
```

代码：

```python
num_features = len(vocab)
num_classes = len(labels)

W = [
    [
        random.uniform(-0.1, 0.1)
        for _ in range(num_features)
    ]
    for _ in range(num_classes)
]

b = [0.0] * num_classes
```

这里：

```text
W
```

实际上是：

```text
3 × vocabulary_size
```

因为我们有三个分类：

```text
device
battery
weather
```

---

## 7. Forward

```python
def forward(x):
    logits = []

    for c in range(num_classes):

        value = b[c]

        for i in range(num_features):
            value += W[c][i] * x[i]

        logits.append(value)

    return softmax(logits)
```

完整过程：

```text
text
 ↓
encode()
 ↓
x
 ↓
W @ x + b
 ↓
logits
 ↓
softmax
 ↓
probabilities
```

---

## 8. Cross Entropy

假设真实答案：

```text
battery
```

模型输出：

```text
[0.1, 0.8, 0.1]
```

我们希望：

```text
battery = 0.8
```

损失：

$$
L=-\log(p_{correct})
$$

所以：

```python
def cross_entropy(probs, target):
    return -math.log(probs[target] + 1e-12)
```

例如：

```text
p = 0.8

loss = -log(0.8)
     ≈ 0.223
```

如果模型非常自信地预测错：

```text
p_correct = 0.01
```

那么：

```text
loss ≈ 4.605
```

所以：

> **预测越错，loss 越大；预测正确且有信心，loss 越小。**

---

## 9. 最关键：反向传播

这里是你真正应该理解的地方。

对于：

```text
softmax + cross entropy
```

有一个非常漂亮的结果：

$$
\frac{\partial L}{\partial z_i}
=
p_i-y_i
$$

也就是：

```text
gradient = prediction - target
```

假设：

```text
prediction:

[0.1, 0.8, 0.1]

target:

[0, 1, 0]
```

那么：

```text
gradient:

[ 0.1, -0.2, 0.1 ]
```

这就是整个分类器学习的核心信号。

---

## 10. 更新 W

因为：

$$
z = Wx+b
$$

所以：

$$
\frac{\partial L}{\partial W}=gradient \times x
$$

代码：

```python
def train_one(x, target, learning_rate=0.1):

    # forward

    probs = forward(x)

    loss = cross_entropy(probs, target)

    # softmax + cross entropy gradient

    dz = probs[:]
    dz[target] -= 1.0

    # update W and b

    for c in range(num_classes):

        for i in range(num_features):

            grad = dz[c] * x[i]

            W[c][i] -= learning_rate * grad

        b[c] -= learning_rate * dz[c]

    return loss
```

这里：

```python
W[c][i] -= learning_rate * grad
```

就是：

> **梯度下降。**

也就是：

```text
参数
 ↓
算出 loss
 ↓
求参数对 loss 的影响
 ↓
往让 loss 下降的方向移动
```

---

## 11. 训练

```python
for epoch in range(1000):

    total_loss = 0.0

    for text, label in samples:

        x = encode(text)

        target = labels[label]

        loss = train_one(x, target)

        total_loss += loss

    if epoch % 100 == 0:
        print(
            f"epoch={epoch}, "
            f"loss={total_loss:.4f}"
        )
```

你应该看到类似：

```text
epoch=0   loss=9.8
epoch=100 loss=1.4
epoch=200 loss=0.7
epoch=300 loss=0.4
...
```

具体数字会因为随机初始化而不同。

---

## 12. 推理

最后：

```python
def predict(text):

    x = encode(text)

    probs = forward(x)

    index = max(
        range(len(probs)),
        key=lambda i: probs[i]
    )

    names = list(labels.keys())

    return names[index], probs
```

然后：

```python
tests = [
    "turn on light",
    "battery level",
    "weather today",
    "battery remaining",
    "open door",
]

for text in tests:

    label, probs = predict(text)

    print(
        text,
        "=>",
        label,
        probs
    )
```

可能得到：

```text
turn on light => device
battery level => battery
weather today => weather
battery remaining => battery
open door => device
```

---

## 13. 你现在实际上已经做出了一个 AI 分类器

整个模型只有：

```text
                  ┌───────────────┐
text              │               │
 │                │               │
 ▼                │               │
Bag of Words ────→│   W x + b     │
                  │               │
                  └───────┬───────┘
                          │
                          ▼
                       Softmax
                          │
                          ▼
                  [device,battery,
                   weather]
```

甚至可以把参数量算出来。

假设：

```text
vocab = 20 words
classes = 3
```

那么：

```text
W = 3 × 20 = 60
b = 3

总参数 = 63
```

**63 个参数。**

而你看到的：

```text
0.6B = 600,000,000
```

是：

```text
6 亿参数
```

两者本质上都在做：

```text
输入
 ↓
参数
 ↓
计算
 ↓
loss
 ↓
gradient
 ↓
更新参数
```

只是复杂度完全不同。

---

## 14. 但这个模型有一个致命问题

现在：

```text
"battery level"
```

和：

```text
"level battery"
```

完全一样。

更严重的是：

```text
"battery"
```

它可能还能识别。

但是：

```text
"我的设备还剩多少电"
```

由于我们的 vocabulary 根本没有：

```text
我的
设备
还剩多少
电
```

所以：

```text
encode()
```

可能直接得到：

```text
[0, 0, 0, ...]
```

模型就傻了。

这就是 **Bag-of-Words 的局限**。

---

## 15. 下一步就进入真正有意思的地方

我们下一版可以把：

```text
Bag-of-Words
```

升级成：

```text
Embedding
```

变成：

```text
文本
 ↓
Token
 ↓
Embedding
 ↓
平均/Pooling
 ↓
Linear
 ↓
Softmax
```

例如：

```text
battery
 ↓
[0.21, -0.83, 0.42, ...]


power
 ↓
[0.18, -0.79, 0.39, ...]
```

于是模型开始能够学习：

```text
battery ≈ power
```

再往后：

```text
Embedding
 ↓
Self Attention
 ↓
Transformer
 ↓
Classification Head
```

最后才是：

```text
0.6B LLM
```

所以整个学习路线其实非常漂亮：

```text
手写 Logistic Regression
        ↓
手写 Softmax Classifier
        ↓
手写 MLP
        ↓
手写 Embedding
        ↓
手写 Attention
        ↓
手写 Transformer Block
        ↓
小型 Transformer 分类器
        ↓
0.6B LLM
        ↓
LLM + 分类器 + Agent
```

**我建议你现在不要跳到 HuggingFace。** 先把上面这个 100 行左右的分类器跑起来，然后我们下一步直接**把它改成“中文文本分类器 + Embedding”**。那一步会真正把“传统机器学习 → 神经网络 NLP”这条线串起来。

# 把它改成中文文本分类器 + Embedding

可以。我们这一步只做一个关键升级：

> **把 `Bag-of-Words` 换成 `Embedding`，但暂时不引入 Transformer。**

这样你能清楚看到 **Embedding 到底是什么、怎么训练、梯度怎么传进去**。

### 1. 模型结构

上一版：

```text
中文文本
 ↓
Bag-of-Words
 ↓
Linear
 ↓
Softmax
```

现在：

```text
中文文本
 ↓
简单分词
 ↓
Token ID
 ↓
Embedding Table
 ↓
平均 Pooling
 ↓
Linear
 ↓
Softmax
 ↓
类别
```

例如：

```text
"还有多少电量"
```

先变成：

```text
["还有", "多少", "电量"]
```

再变成：

```text
[3, 7, 12]
```

Embedding 表：

```text
E =
token 0 → [ 0.12, -0.31,  0.55, ...]
token 1 → [-0.72,  0.18,  0.22, ...]
token 2 → [ 0.33,  0.44, -0.19, ...]
...
```

于是：

```text
[3, 7, 12]
       ↓
E[3], E[7], E[12]
       ↓
   average
       ↓
一个句子向量
       ↓
Linear
```

---

## 2. 为什么叫 Embedding？

本质上就是一个二维数组：

```python
embedding = [
    [0.1, 0.2, ...],   # token 0
    [0.3, 0.7, ...],   # token 1
    ...
]
```

假设：

```text
词表大小 = 100
embedding dimension = 8
```

那么：

```text
Embedding Shape = [100, 8]
```

也就是：

```text
100 个 token
×
每个 token 8 个数字
```

**Embedding 本身一开始没有任何语义。**

它只是随机数字：

```text
电量 → [0.13, -0.72, 0.41, ...]
天气 → [-0.31, 0.82, 0.05, ...]
```

训练过程中，梯度会不断修改这些数字，最终模型发现：

```text
电量
电池
剩余电量
```

应该产生比较有利于同一分类的表示。

---

## 3. 先限定我们的任务

我们做一个 ESP32/Agent 风格的中文意图分类器：

```text
设备控制
电量查询
天气查询
```

训练数据：

```python
samples = [
    ("打开客厅灯", "device"),
    ("关闭客厅灯", "device"),
    ("把灯打开", "device"),
    ("打开卧室的灯", "device"),
    ("关掉灯", "device"),

    ("还有多少电", "battery"),
    ("电池还剩多少", "battery"),
    ("当前电量是多少", "battery"),
    ("看看电池电量", "battery"),
    ("设备还有多少电量", "battery"),

    ("今天天气怎么样", "weather"),
    ("明天天气如何", "weather"),
    ("今天会下雨吗", "weather"),
    ("现在天气怎么样", "weather"),
    ("明天会不会下雨", "weather"),
]
```

---

## 4. 中文 Tokenizer

这里我们**暂时不用 jieba**，因为我们是在学习原理。

最简单的方法：

```text
打开客厅灯
```

直接拆成：

```text
["打", "开", "客", "厅", "灯"]
```

代码：

```python
def tokenize(text):
    return list(text)
```

所以：

```python
tokenize("打开客厅灯")
```

得到：

```text
['打', '开', '客', '厅', '灯']
```

这不是一个优秀的中文 tokenizer，但对于学习 Embedding 非常合适。

---

## 5. 建立 Vocabulary

```python
vocab = {
    "<UNK>": 0
}

for text, _ in samples:
    for token in tokenize(text):
        if token not in vocab:
            vocab[token] = len(vocab)

print(vocab)
```

例如：

```text
打 → 1
开 → 2
客 → 3
厅 → 4
灯 → 5
...
```

`<UNK>` 表示：

> Unknown Token，训练过程中没有见过的字符。

---

## 6. 文本 → Token ID

```python
def encode(text):
    return [
        vocab.get(token, vocab["<UNK>"])
        for token in tokenize(text)
    ]
```

例如：

```python
encode("打开客厅灯")
```

可能得到：

```text
[1, 2, 3, 4, 5]
```

到这里：

```text
文本
 ↓
字符
 ↓
整数 ID
```

---

## 7. 手写 Embedding

现在是核心。

假设：

```python
embedding_dim = 8
```

创建：

```python
import random

embedding = [
    [
        random.uniform(-0.1, 0.1)
        for _ in range(embedding_dim)
    ]
    for _ in range(len(vocab))
]
```

假设：

```text
vocab_size = 50
embedding_dim = 8
```

那么：

```text
embedding.shape = [50, 8]
```

例如：

```text
embedding[5]
```

可能是：

```text
[0.03, -0.12, 0.44, 0.18, -0.31, 0.07, 0.22, -0.04]
```

---

## 8. Token ID → Embedding

```python
def embedding_forward(token_ids):
    vectors = []

    for token_id in token_ids:
        vectors.append(embedding[token_id])

    return vectors
```

例如：

```text
"打开客厅灯"
```

变成：

```text
[1, 2, 3, 4, 5]
```

然后：

```text
Embedding
    ↓
[
 E[1],
 E[2],
 E[3],
 E[4],
 E[5]
]
```

也就是：

```text
5 × 8
```

的矩阵。

---

## 9. 但 Linear 需要一个固定长度向量

句子长度不一样：

```text
"开灯"

2 tokens
```

而：

```text
"打开客厅的灯"

6 tokens
```

不能直接送进同一个 Linear。

所以我们做一个非常简单的：

> **Mean Pooling**

也就是求平均。

```python
def mean_pool(vectors):
    result = [0.0] * embedding_dim

    if not vectors:
        return result

    for vector in vectors:
        for i in range(embedding_dim):
            result[i] += vector[i]

    n = len(vectors)

    for i in range(embedding_dim):
        result[i] /= n

    return result
```

于是：

```text
"打开客厅灯"
       ↓
5 × 8 Embedding
       ↓
Mean
       ↓
1 × 8
```

---

## 10. 接 Linear

现在我们的输入不再是：

```text
Bag-of-Words
```

而是：

```text
8 维句子向量
```

所以：

```python
num_features = embedding_dim
num_classes = 3
```

权重：

```python
W = [
    [
        random.uniform(-0.1, 0.1)
        for _ in range(num_features)
    ]
    for _ in range(num_classes)
]

b = [0.0] * num_classes
```

仍然是：

$$
z = Wx+b
$$

---

## 11. Forward

```python
def forward(text):

    token_ids = encode(text)

    vectors = embedding_forward(token_ids)

    x = mean_pool(vectors)

    logits = []

    for c in range(num_classes):

        value = b[c]

        for i in range(num_features):
            value += W[c][i] * x[i]

        logits.append(value)

    probs = softmax(logits)

    return probs, token_ids, x
```

整个过程：

```text
                    "还有多少电"
                          │
                          ▼
                 ["还","有","多","少","电"]
                          │
                          ▼
                    Token IDs
                          │
                          ▼
                     Embedding
                          │
                          ▼
                     Mean Pool
                          │
                          ▼
                    Sentence Vector
                          │
                          ▼
                       Linear
                          │
                          ▼
                      Softmax
                          │
                          ▼
              [device,battery,weather]
```

---

## 12. 最有意思的地方：Embedding 也要训练

上一版我们只更新：

```text
W
b
```

现在还必须更新：

```text
Embedding
```

因为：

```text
Embedding
    ↓
Mean
    ↓
Linear
    ↓
Loss
```

所以 Loss 的梯度必须一路反向传播：

```text
Loss
 ↓
Linear
 ↓
Mean
 ↓
Embedding
```

---

## 13. Linear 的梯度

我们仍然：

```python
dz = probs[:]
dz[target] -= 1.0
```

然后：

```python
for c in range(num_classes):

    for i in range(embedding_dim):

        W[c][i] -= learning_rate * dz[c] * x[i]

    b[c] -= learning_rate * dz[c]
```

这和上一版完全一样。

---

## 14. 梯度怎么回到 Embedding？

Linear：

$$
z = Wx
$$

所以：

$$
\frac{\partial L}{\partial x}
=
W^T\frac{\partial L}{\partial z}
$$

代码：

```python
dx = [0.0] * embedding_dim

for i in range(embedding_dim):

    for c in range(num_classes):

        dx[i] += W[c][i] * dz[c]
```

现在我们得到了：

```text
dx
```

也就是：

> **句子向量 x 的梯度。**

---

## 15. 再穿过 Mean Pooling

假设：

```text
"打开客厅灯"
```

有 5 个 token：

```text
E1
E2
E3
E4
E5
```

Mean：

$$
x=\frac{E_1+E_2+E_3+E_4+E_5}{5}
$$

所以每个 Embedding 得到：

$$
\frac{\partial L}{\partial E_i}
=
\frac{1}{5}
\frac{\partial L}{\partial x}
$$

代码：

```python
n = len(token_ids)

for token_id in token_ids:

    for i in range(embedding_dim):

        grad = dx[i] / n

        embedding[token_id][i] -= (
            learning_rate * grad
        )
```

这几行非常重要。

因为它意味着：

```text
"打开客厅灯"
```

训练一次以后：

```text
"打" 的向量会变化
"开" 的向量会变化
"客" 的向量会变化
"厅" 的向量会变化
"灯" 的向量会变化
```

---

## 16. 完整训练函数

把它们合起来：

```python
def train_one(text, target, learning_rate=0.05):

    # ---------- forward ----------

    probs, token_ids, x = forward(text)

    loss = cross_entropy(probs, target)

    # ---------- softmax gradient ----------

    dz = probs[:]
    dz[target] -= 1.0

    # ---------- W / b gradient ----------

    dx = [0.0] * embedding_dim

    for c in range(num_classes):

        for i in range(embedding_dim):

            dx[i] += W[c][i] * dz[c]

            W[c][i] -= (
                learning_rate
                * dz[c]
                * x[i]
            )

        b[c] -= learning_rate * dz[c]

    # ---------- Embedding gradient ----------

    n = len(token_ids)

    for token_id in token_ids:

        for i in range(embedding_dim):

            grad = dx[i] / n

            embedding[token_id][i] -= (
                learning_rate * grad
            )

    return loss
```

现在你的模型已经是：

```text
       Embedding
           │
           ▼
      Mean Pooling
           │
           ▼
         Linear
           │
           ▼
        Softmax
           │
           ▼
        CrossEntropy
           │
           │ backward
           ▼
       更新所有参数
```

---

## 17. 完整代码

为了方便你直接跑，我把它合成一个文件：

```python
import math
import random


## ============================================================
## Dataset
## ============================================================

samples = [
    ("打开客厅灯", "device"),
    ("关闭客厅灯", "device"),
    ("把灯打开", "device"),
    ("打开卧室的灯", "device"),
    ("关掉灯", "device"),

    ("还有多少电", "battery"),
    ("电池还剩多少", "battery"),
    ("当前电量是多少", "battery"),
    ("看看电池电量", "battery"),
    ("设备还有多少电量", "battery"),

    ("今天天气怎么样", "weather"),
    ("明天天气如何", "weather"),
    ("今天会下雨吗", "weather"),
    ("现在天气怎么样", "weather"),
    ("明天会不会下雨", "weather"),
]


## ============================================================
## Tokenizer
## ============================================================

def tokenize(text):
    return list(text)


## ============================================================
## Vocabulary
## ============================================================

vocab = {
    "<UNK>": 0
}

for text, _ in samples:

    for token in tokenize(text):

        if token not in vocab:
            vocab[token] = len(vocab)


## ============================================================
## Labels
## ============================================================

labels = {
    "device": 0,
    "battery": 1,
    "weather": 2,
}

num_classes = len(labels)


## ============================================================
## Embedding
## ============================================================

embedding_dim = 8

embedding = [
    [
        random.uniform(-0.1, 0.1)
        for _ in range(embedding_dim)
    ]
    for _ in range(len(vocab))
]


## ============================================================
## Classifier
## ============================================================

W = [
    [
        random.uniform(-0.1, 0.1)
        for _ in range(embedding_dim)
    ]
    for _ in range(num_classes)
]

b = [0.0] * num_classes


## ============================================================
## Utils
## ============================================================

def encode(text):

    return [
        vocab.get(token, vocab["<UNK>"])
        for token in tokenize(text)
    ]


def softmax(xs):

    max_x = max(xs)

    exps = [
        math.exp(x - max_x)
        for x in xs
    ]

    total = sum(exps)

    return [
        x / total
        for x in exps
    ]


def cross_entropy(probs, target):

    return -math.log(
        probs[target] + 1e-12
    )


## ============================================================
## Forward
## ============================================================

def forward(text):

    token_ids = encode(text)

    # Embedding lookup

    vectors = [
        embedding[token_id]
        for token_id in token_ids
    ]

    # Mean pooling

    x = [0.0] * embedding_dim

    for vector in vectors:

        for i in range(embedding_dim):

            x[i] += vector[i]

    if vectors:

        for i in range(embedding_dim):

            x[i] /= len(vectors)

    # Linear

    logits = []

    for c in range(num_classes):

        value = b[c]

        for i in range(embedding_dim):

            value += W[c][i] * x[i]

        logits.append(value)

    probs = softmax(logits)

    return probs, token_ids, x


## ============================================================
## Training
## ============================================================

def train_one(
    text,
    target,
    learning_rate=0.05
):

    # Forward

    probs, token_ids, x = forward(text)

    loss = cross_entropy(
        probs,
        target
    )

    # dL / dz

    dz = probs[:]

    dz[target] -= 1.0

    # dL / dx

    dx = [0.0] * embedding_dim

    for c in range(num_classes):

        for i in range(embedding_dim):

            dx[i] += W[c][i] * dz[c]

    # Update W / b

    for c in range(num_classes):

        for i in range(embedding_dim):

            W[c][i] -= (
                learning_rate
                * dz[c]
                * x[i]
            )

        b[c] -= (
            learning_rate
            * dz[c]
        )

    # Update Embedding

    n = len(token_ids)

    if n > 0:

        for token_id in token_ids:

            for i in range(embedding_dim):

                grad = dx[i] / n

                embedding[token_id][i] -= (
                    learning_rate
                    * grad
                )

    return loss


## ============================================================
## Train
## ============================================================

for epoch in range(1000):

    total_loss = 0.0

    for text, label in samples:

        loss = train_one(
            text,
            labels[label]
        )

        total_loss += loss

    if epoch % 100 == 0:

        print(
            f"epoch={epoch}, "
            f"loss={total_loss:.4f}"
        )


## ============================================================
## Inference
## ============================================================

label_names = list(labels.keys())


def predict(text):

    probs, _, _ = forward(text)

    index = max(
        range(num_classes),
        key=lambda i: probs[i]
    )

    return (
        label_names[index],
        probs
    )


## ============================================================
## Test
## ============================================================

tests = [
    "打开灯",
    "关闭灯",
    "还有多少电",
    "电池电量",
    "今天下雨吗",
    "明天天气",
    "我的电池还剩多少",
]

for text in tests:

    label, probs = predict(text)

    print(
        text,
        "=>",
        label,
        probs
    )
```

---

## 18. 但是现在有一个很重要的问题

你运行：

```text
"我的电池还剩多少"
```

**不一定能正确分类。**

原因不是模型太小，而是我们的 tokenizer 太原始：

```text
我
的
电
池
还
剩
多
少
```

它只是字符级。

这反而是一个非常好的学习点：

#### Embedding ≠ 理解语言

Embedding 只是：

```text
ID → 向量
```

真正的语言理解来自后面的模型结构。

现在：

```text
Embedding
   ↓
Mean
   ↓
Linear
```

它连词序都不知道。

例如：

```text
"灯打开"
```

和：

```text
"打开灯"
```

经过 Mean Pooling 后，本质上几乎完全一样：

```text
E["灯"] + E["打开"]
```

顺序消失了。

---

## 19. 下一步为什么必须学习 Attention

这正好把我们引向 Transformer。

现在：

```text
Embedding
 ↓
Mean Pooling
 ↓
Linear
```

丢失了：

* 词序
* 上下文
* token 之间的关系

Transformer 则变成：

```text
Token
 ↓
Embedding
 ↓
Position
 ↓
Self-Attention
 ↓
Feed Forward
 ↓
...
 ↓
Classification Head
```

Self-Attention 最核心的一件事情是：

> **一个 token 可以动态地“看”其他 token。**

例如：

```text
"打开客厅灯"
```

模型可以学习：

```text
打开 ─────→ 灯
  │
  └────→ 客厅
```

而不是简单地：

```text
平均所有字符
```

---

### 你现在应该重点理解的 4 个东西

如果这版代码跑通了，不要急着优化，先确认你真的理解：

```text
① Embedding 是一个可训练的矩阵

② Token ID 只是索引，不是语义

③ Mean Pooling 把多个 token 向量压成一个句子向量

④ Embedding 也参与反向传播
```

其中第 **④** 最重要。

因为你刚才已经亲手实现了：

$$
Loss
\rightarrow Linear
\rightarrow Pooling
\rightarrow Embedding
$$

这就是神经网络训练的核心机制。

下一步最值得做的是**不使用 PyTorch，继续手写一个最小 Self-Attention**。这样你会看到 `Q / K / V` 为什么会出现，以及它到底是怎么替代现在这个 `Mean Pooling` 的。

# 帮我手写一个最小 Self-Attention


可以。我们就在你上一版 **Embedding + Mean Pooling** 上继续升级。

核心目标不是先做一个能用的 Transformer，而是**手写出 Self-Attention 最小数学闭环**：

```text
Token
 ↓
Embedding
 ↓
Q / K / V
 ↓
QKᵀ / √d
 ↓
Softmax
 ↓
Attention × V
 ↓
新的 Token 表示
```

你理解这套以后，Transformer 的核心就已经打开了。

---

## 1. 先理解：Attention 到底解决什么问题？

你上一版是：

```text
"打开客厅灯"

Embedding
   ↓
E["打"]
E["开"]
E["客"]
E["厅"]
E["灯"]
   ↓
Mean
   ↓
一个句向量
```

问题是：

```text
"打开灯"
```

和：

```text
"灯打开"
```

经过 Mean 后，本质上是同一堆向量相加。

**词序和 token 之间的关系丢失了。**

Self-Attention 的思路是：

> 每个 token 都问一遍：**“我现在应该关注其他哪些 token？”**

例如：

```text
打开 客厅 灯
 │    │    │
 └────┼────┘
      │
      ▼
   Attention
```

“打开”可能更关注“灯”。

“客厅”也可能更关注“灯”。

于是每个 token 都会得到一个**结合上下文后的新表示**。

---

## 2. 最小 Self-Attention

先完全抛开训练。

假设有 3 个 token：

```text
X =
[
    [1, 0],
    [0, 1],
    [1, 1]
]
```

也就是：

```text
token1 = [1, 0]
token2 = [0, 1]
token3 = [1, 1]
```

我们希望得到：

```text
输出 =
[
    新 token1,
    新 token2,
    新 token3
]
```

---

## 3. Q / K / V 是什么？

这是第一次学 Attention 最容易混乱的地方。

不要把它想得太复杂。

可以暂时理解成：

```text
Q = Query
K = Key
V = Value
```

每个 token 都生成三份东西：

```text
                ┌── Q：我想找什么？
Token ──────────┼── K：我有什么特征？
                └── V：如果别人关注我，我提供什么信息？
```

数学上：

$$
Q=XW_Q
$$

$$
K=XW_K
$$

$$
V=XW_V
$$

其中：

```text
WQ
WK
WV
```

都是**可训练参数**。

---

## 4. 第一版我们甚至可以不训练 WQ/WK/WV

为了理解原理，先直接：

```python
Q = X
K = X
V = X
```

也就是：

```text
WQ = I
WK = I
WV = I
```

这样可以把 Attention 的核心完全暴露出来。

---

## 5. 第一步：Q × Kᵀ

假设：

```text
Q =
[
 [1, 0],
 [0, 1],
 [1, 1]
]
```

K 一样。

计算：

$$
S=QK^T
$$

代码：

```python
def matmul(A, B):
    rows = len(A)
    cols = len(B[0])
    inner = len(B)

    result = [
        [0.0] * cols
        for _ in range(rows)
    ]

    for i in range(rows):
        for j in range(cols):
            for k in range(inner):
                result[i][j] += A[i][k] * B[k][j]

    return result


def transpose(A):
    return [
        list(row)
        for row in zip(*A)
    ]
```

然后：

```python
scores = matmul(Q, transpose(K))
```

得到：

```text
[
 [1, 0, 1],
 [0, 1, 1],
 [1, 1, 2]
]
```

---

## 6. 这个矩阵是什么意思？

这是 Attention 最关键的一步。

```text
        K1   K2   K3

Q1      1    0    1
Q2      0    1    1
Q3      1    1    2
```

例如第一行：

```text
[1, 0, 1]
```

表示：

```text
Q1 和 K1 → 相似度 1
Q1 和 K2 → 相似度 0
Q1 和 K3 → 相似度 1
```

所以：

> **QKᵀ 本质上是在计算 token 与 token 之间的相关程度。**

---

## 7. 为什么除以 √d？

Transformer 不直接使用：

```text
QKᵀ
```

而是：

$$
S=\frac{QK^T}{\sqrt{d_k}}
$$

这里：

```text
d_k = Key 的维度
```

如果：

```text
d_k = 64
```

就除以：

```text
√64 = 8
```

代码：

```python
import math

def scale_scores(scores, dim):

    scale = math.sqrt(dim)

    return [
        [
            value / scale
            for value in row
        ]
        for row in scores
    ]
```

为什么？

因为维度很大时：

```text
Q · K
```

的数值可能越来越大。

然后进入 Softmax：

```text
exp(很大的数字)
```

容易导致：

```text
softmax
↓
几乎 one-hot
```

梯度也容易变得不好。

所以：

```text
QKᵀ / √d
```

是一种数值尺度控制。

---

## 8. Softmax

现在：

```text
scores
```

变成：

```text
[
 [0.707, 0, 0.707],
 [0, 0.707, 0.707],
 [0.707, 0.707, 1.414]
]
```

接下来每一行做 Softmax。

注意：

> **每一行单独 Softmax。**

代码：

```python
def softmax_row(row):

    max_value = max(row)

    exps = [
        math.exp(x - max_value)
        for x in row
    ]

    total = sum(exps)

    return [
        x / total
        for x in exps
    ]


def softmax_matrix(matrix):

    return [
        softmax_row(row)
        for row in matrix
    ]
```

得到类似：

```text
[
 [0.401, 0.198, 0.401],
 [0.198, 0.401, 0.401],
 [0.248, 0.248, 0.503]
]
```

这就是：

> **Attention Weights**

---

## 9. 这个矩阵才是 Self-Attention 的灵魂

假设：

```text
A =
[
 [0.4, 0.2, 0.4],
 [0.2, 0.4, 0.4],
 [0.25,0.25,0.5]
]
```

可以把它看成：

```text
             我应该关注谁？

          T1     T2     T3
T1       0.4    0.2    0.4
T2       0.2    0.4    0.4
T3       0.25   0.25   0.5
```

比如：

```text
T1
```

最终会：

```text
40% × V1
20% × V2
40% × V3
```

所以：

> **Attention = 根据相关性，对其他 token 的信息进行加权平均。**

这句话非常重要。

---

## 10. 最后一步：Attention × V

数学公式：

$$
Output = Attention \cdot V
$$

代码：

```python
output = matmul(attention, V)
```

完整 Attention：

```python
def self_attention(X):

    Q = X
    K = X
    V = X

    # QK^T

    scores = matmul(
        Q,
        transpose(K)
    )

    # scaling

    scores = scale_scores(
        scores,
        len(K[0])
    )

    # softmax

    attention = softmax_matrix(
        scores
    )

    # weighted sum

    output = matmul(
        attention,
        V
    )

    return output, attention
```

这就是一个**真正的 Self-Attention**。

没有 PyTorch。

没有 Transformer 库。

没有黑盒。

---

## 11. 用一个实际例子

假设：

```python
X = [
    [1.0, 0.0],
    [0.0, 1.0],
    [1.0, 1.0],
]
```

运行：

```python
output, attention = self_attention(X)

print("attention:")
for row in attention:
    print(row)

print("output:")
for row in output:
    print(row)
```

你会看到类似：

```text
attention:
[0.401, 0.198, 0.401]
[0.198, 0.401, 0.401]
[0.248, 0.248, 0.503]
```

然后：

```text
output:
[0.802, 0.599]
[0.599, 0.802]
[0.751, 0.751]
```

注意一个非常关键的变化：

输入：

```text
T1 = [1, 0]
```

输出：

```text
T1 = [0.802, 0.599]
```

它已经不再只是自己的信息。

而是：

```text
T1
 ↓
关注 T1 / T2 / T3
 ↓
混合其他 token 信息
 ↓
新的 T1
```

这就是 Context。

---

## 12. 为什么叫 Self-Attention？

因为：

```text
Q
K
V
```

全部来自：

```text
同一个 X
```

即：

```text
X
├──→ Q
├──→ K
└──→ V
```

所以叫：

> **Self-Attention**

如果 Q 来自一个序列，而 K/V 来自另一个序列，就是：

> Cross-Attention

---

## 13. 现在把 Q/K/V 变成真正可训练的

刚才为了学习，我们用了：

```python
Q = X
K = X
V = X
```

真正 Transformer 是：

```text
X
 │
 ├── Linear(WQ) → Q
 │
 ├── Linear(WK) → K
 │
 └── Linear(WV) → V
```

也就是：

$$
Q=XW_Q
$$

$$
K=XW_K
$$

$$
V=XW_V
$$

我们手写一个 Linear：

```python
def linear(X, W):

    return matmul(X, W)
```

假设：

```python
X = [
    [0.2, 0.5, 0.1, 0.7],
    [0.8, 0.1, 0.3, 0.2],
    [0.4, 0.6, 0.9, 0.1],
]
```

然后：

```python
WQ = random_matrix(4, 4)
WK = random_matrix(4, 4)
WV = random_matrix(4, 4)

Q = linear(X, WQ)
K = linear(X, WK)
V = linear(X, WV)
```

---

## 14. 完整版本

现在可以把真正的结构写出来：

```python
import math
import random


def matmul(A, B):

    rows = len(A)
    cols = len(B[0])
    inner = len(B)

    result = [
        [0.0] * cols
        for _ in range(rows)
    ]

    for i in range(rows):

        for j in range(cols):

            for k in range(inner):

                result[i][j] += (
                    A[i][k] * B[k][j]
                )

    return result


def transpose(A):

    return [
        list(row)
        for row in zip(*A)
    ]


def random_matrix(rows, cols):

    return [
        [
            random.uniform(-0.1, 0.1)
            for _ in range(cols)
        ]
        for _ in range(rows)
    ]


def softmax_row(row):

    maximum = max(row)

    exps = [
        math.exp(x - maximum)
        for x in row
    ]

    total = sum(exps)

    return [
        x / total
        for x in exps
    ]


def softmax_matrix(matrix):

    return [
        softmax_row(row)
        for row in matrix
    ]


def self_attention(X):

    dim = len(X[0])

    # Learnable parameters

    WQ = random_matrix(dim, dim)
    WK = random_matrix(dim, dim)
    WV = random_matrix(dim, dim)

    # Q K V

    Q = matmul(X, WQ)

    K = matmul(X, WK)

    V = matmul(X, WV)

    # QK^T

    scores = matmul(
        Q,
        transpose(K)
    )

    # Scale

    scale = math.sqrt(dim)

    for i in range(len(scores)):

        for j in range(len(scores[i])):

            scores[i][j] /= scale

    # Softmax

    attention = softmax_matrix(
        scores
    )

    # Attention × V

    output = matmul(
        attention,
        V
    )

    return output, attention
```

这里有一个**重要问题**：

```python
WQ = random_matrix(...)
```

如果放在：

```python
self_attention()
```

里面，那么每次调用都会重新随机生成参数。

**真正训练时绝对不能这么做。**

应该：

```python
WQ
WK
WV
```

作为模型参数长期保存。

所以正式模型应该类似：

```python
class SelfAttention:

    def __init__(self, dim):

        self.WQ = random_matrix(dim, dim)
        self.WK = random_matrix(dim, dim)
        self.WV = random_matrix(dim, dim)

    def forward(self, X):

        Q = matmul(X, self.WQ)
        K = matmul(X, self.WK)
        V = matmul(X, self.WV)

        scores = matmul(
            Q,
            transpose(K)
        )

        scale = math.sqrt(len(K[0]))

        for i in range(len(scores)):
            for j in range(len(scores[i])):
                scores[i][j] /= scale

        attention = softmax_matrix(scores)

        output = matmul(
            attention,
            V
        )

        return output, attention
```

---

## 15. 到这里，你应该看到一个很漂亮的演化

我们之前：

```text
中文
 ↓
Token
 ↓
Embedding
 ↓
Mean
 ↓
Linear
 ↓
Softmax
```

现在：

```text
中文
 ↓
Token
 ↓
Embedding
 ↓
┌─────────────────────┐
│   Self-Attention     │
│                     │
│ X → Q               │
│ X → K               │
│ X → V               │
│                     │
│ QKᵀ                 │
│ ↓                   │
│ /√d                 │
│ ↓                   │
│ Softmax             │
│ ↓                   │
│ × V                 │
└─────────┬───────────┘
          ↓
       Context
          ↓
       Linear
          ↓
       Softmax
```

---

## 16. 还有一个你现在必须注意的问题：它仍然不知道顺序

即使有 Self-Attention：

```text
"打开灯"
```

和：

```text
"灯打开"
```

如果输入 Embedding 完全一样，只是交换位置，那么 Attention 本身仍然无法知道：

```text
第一个 token
```

和：

```text
第二个 token
```

的区别。

所以 Transformer 还需要：

```text
Positional Encoding
```

也就是：

```text
Embedding
+
Position
↓
Transformer
```

例如：

```text
打开 灯
 ↓   ↓
E0  E1

灯 打开
 ↓   ↓
E0  E1
```

通过位置编码以后：

```text
打开 = token embedding + position 0
灯   = token embedding + position 1
```

和：

```text
灯   = token embedding + position 0
打开 = token embedding + position 1
```

就不一样了。

---

## 17. 所以 Transformer 的最小完整结构

我们现在已经走到这里：

```text
              Token IDs
                  │
                  ▼
              Embedding
                  │
                  ▼
         + Positional Encoding
                  │
                  ▼
            ┌───────────┐
            │   Q = XWQ │
            │   K = XWK │
            │   V = XWV │
            └─────┬─────┘
                  │
                  ▼
               QKᵀ / √d
                  │
                  ▼
                Softmax
                  │
                  ▼
                 × V
                  │
                  ▼
           Attention Output
                  │
                  ▼
            Feed Forward
                  │
                  ▼
             Classifier
                  │
                  ▼
              Category
```

**下一步最值得手写的是 `Positional Encoding + Multi-Head Attention + 一个最小 Transformer Block`。**

尤其是 Multi-Head 不需要把它想得很神秘：本质上就是**把 embedding 维度切成几个头，每个头独立做一次 Q/K/V Attention，然后拼回来**。这一步做完，你就已经从“手写 NLP 分类器”真正走进 Transformer 内部了。
