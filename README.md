# 原料报价仓 · 有序邻近关联与分片边界

这里保存园区成本、原料及供销资料的基础读取接口，样例值为开发用合成记录，不对应真实交易。asof.py只判断单对资格与优先级，streams.py提供不可重放的输入流；尚无邻近连接计划及执行。

`lake/asof.py`、`lake/streams.py`描述当前接口。`lake/storage.py`使用有序JSON编码、SHA256内容身份及不可变正文；`data/source.json`保存现有资料。字段约定见[资料契约](docs/contracts.md)，字段缺失与显式null不同。

使用Python 3.11。依赖在requirements.txt固定，空清单表示仅标准库。

```sh
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m compileall -q lake tests
python -m lake
```

以上入口读取当前资料及检查已有接口。它不执行新增查询，输出资料分区名称和正文摘要。可在Linux容器执行相同入口：

```sh
docker build -t park-lake .
docker run --rm --network=none park-lake python -m unittest discover -s tests -v
docker run --rm --network=none park-lake python -m lake
```

运行生成的正文与临时文件存放在`.runtime/`；不得把本机配置或凭据放入资料正文。
