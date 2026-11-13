# 资料语义与接口边界

left的键为(product,source,t)，right同键另有priority和row_id。product/source任一null不匹配；left.t=null未匹配，right.t=null不参与。direction为backward/forward/nearest；allow_exact控制t相等是否可用；tolerance为非负整数且包含边界。nearest距离相同时先选较早时刻，同刻再按priority降序、row_id的UTF-8升序；backward/forward同刻也用此规则。所有left物理行保留一次，右行可被多次复用，不消耗。asof.py已有单候选资格函数和排序规则，不提供找最近的执行器。输出matched、right_row_id、distance和左右快照。内存上限按保留行字节计，热点或同刻组不豁免；允许外排和持久索引，引用绑定源摘要。

asof.py只判断单对资格与优先级，streams.py提供不可重放的输入流；尚无邻近连接计划及执行。

正文摘要绑定完整值，样例数据不限定输入规模；错误不等同空结果，接口使用中文错误说明。
