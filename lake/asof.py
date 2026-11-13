"""报价候选资格和同刻优先级。"""
from .storage import digest

def validate_options(direction,tolerance,allow_exact):
    if direction not in ('backward','forward','nearest'):raise ValueError('未知邻近方向')
    if type(tolerance) is not int or tolerance<0:raise ValueError('容差应为非负整数')
    if type(allow_exact) is not bool:raise ValueError('精确匹配选项非法')

def candidate(left,right,direction='backward',tolerance=0,allow_exact=True):
    validate_options(direction,tolerance,allow_exact)
    for key in ('product','source'):
        if left[key] is None or right[key] is None or left[key]!=right[key]:return False
    a,b=left['t'],right['t']
    if a is None or b is None:return False
    if type(a) is not int or type(b) is not int:raise ValueError('时间应为整数')
    if a==b and not allow_exact:return False
    if direction=='backward' and b>a:return False
    if direction=='forward' and b<a:return False
    return abs(a-b)<=tolerance

def preference(left,right,direction):
    validate_options(direction,0,True)
    delta=right['t']-left['t']
    first=(abs(delta),right['t']) if direction=='nearest' else ((-right['t'],) if direction=='backward' else (right['t'],))
    return first+(-right['priority'],right['row_id'].encode('utf-8'))

def partition_manifest(rows):
    return {'digest':digest(rows),'count':len(rows),'row_ids':[r['row_id'] for r in rows]}
