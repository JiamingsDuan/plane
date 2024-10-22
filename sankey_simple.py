from pyecharts import options as opts
from pyecharts.charts import Sankey

# nodes = [
#     {"name": "category1"},
#     {"name": "category2"},
#     {"name": "category3"},
#     {"name": "category4"},
#     {"name": "category5"},
#     {"name": "category6"},
# ]
#
# links = [
#     {"source": "category1", "target": "category2", "value": 1},
#     {"source": "category2", "target": "category3", "value": 1},
#     {"source": "category3", "target": "category4", "value": 2},
# {"source": "category2", "target": "category5", "value": 2},
#     {"source": "category1", "target": "category6", "value": 1},
# ]
# c = (
#     Sankey()
#     .add(
#         "sankey",
#         nodes,
#         links,
#         linestyle_opt=opts.LineStyleOpts(opacity=0.2, curve=0.5, color="source"),
#         label_opts=opts.LabelOpts(position="bottom"),
#         # orient="vertical",
#     )
#     .set_global_opts(title_opts=opts.TitleOpts(title="Sankey-基本示例"))
#     .render("htm/sankey_base.html")
# )
import math

"""
要计算两条路径之间的 Fréchet 距离（Fréchet Distance），你可以使用递归方法、动态规划，或者利用现有的库。以下是一个详细的示例，展示如何使用纯 Python 实现 Fréchet 距离的计算。

使用纯 Python 实现 Fréchet 距离
下面的代码实现了 Fréchet 距离的递归和动态规划方法。函数接受两条路径（分别由一系列的点表示）并计算它们之间的 Fréchet 距离。
"""
import math


def euclidean_distance(p1, p2):
    """计算两个点之间的欧几里得距离"""
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def frechet_distance(curve1, curve2):
    """计算两条路径之间的 Fréchet 距离"""
    n = len(curve1)
    m = len(curve2)
    # 创建一个 memo 表，用于存储计算结果
    memo = [[-1] * m for _ in range(n)]

    def helper(i, j):
        if memo[i][j] != -1:
            return memo[i][j]

        # 到达两条曲线的末尾
        if i == n - 1 and j == m - 1:
            return euclidean_distance(curve1[i], curve2[j])

        # 只剩下 curve1
        if i == n - 1:
            return max(helper(i, j + 1), euclidean_distance(curve1[i], curve2[j]))
        # 只剩下 curve2
        if j == m - 1:
            return max(helper(i + 1, j), euclidean_distance(curve1[i], curve2[j]))

        # 递归计算
        res = max(
            min(helper(i + 1, j), helper(i, j + 1), helper(i + 1, j + 1)),
            euclidean_distance(curve1[i], curve2[j])
        )

        memo[i][j] = res
        return res

    return helper(0, 0)


# 示例路径
curve1 = [(0, 0), (1, 1), (2, 2)]
curve2 = [(0, 1), (1, 2), (2, 3)]

# 计算 Fréchet 距离
print("Fréchet 距离:", frechet_distance(curve1, curve2))
"""

解释
欧几里得距离：euclidean_distance 函数计算两个点之间的距离。
Fréchet 距离：
frechet_distance 函数初始化一个 memo 表，用于存储之前计算的结果以加速计算。
helper 是一个递归函数，结合了动态规划的思想。
如果到达了最后一个点，就算出该点之间的距离。
如果一条曲线已经遍历完，就继续计算另一条曲线的距离。
遍历所有可能的路径，最终取最大值作为 Fréchet 距离的一部分。
示例路径：使用 curve1 和 curve2 定义了两个路径，最后计算并输出它们之间的 Fréchet 距离。
注意事项
上述实现对于较短的路径是有效的，但在处理长路径时可能效率较低。可以考虑进一步优化（例如，通过迭代动态规划方法）。
可以使用开源库（如 scipy）来获取更高效的算法实现。
结论
这段代码提供了一个如何用 Python 计算两条路径 Fréchet 距离的简单示例。你可以根据具体需求进行修改和扩展。
"""
