# 从书库看MBTI

[MyBooks](https://mybooks.top) 工具箱外置工具：读取书库书籍的分类和标签，根据类型关键词统计结果，趣味推测用户的 MBTI 类型。

- 工具 ID：`mbti_tester`
- 语言：简体中文
- Core API：`1.3.0`
- 只读操作：不会更改书籍、分类或标签
- 重要说明：结果是娱乐推测，不是心理测验或专业人格评估

## 开发与安装

前端是无需构建的静态页面，后端从 [Core API](https://mybookstop.github.io/docs/manual/tool-development) 分批读取分类与标签。运行分析逻辑的本地单元测试：

```bash
python -m unittest discover -s tests
```

校验与打包需要安装 MyBooks Tools Builder：

```bash
mytool validate .
mytool build
```

在启用开发者模式的 MyBooks 管理工具箱上传生成的 ZIP；安装或更新后重启 MyBooks。
