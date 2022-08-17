import re  # 正则表达式，进行文字匹配`

# 查询规则
findAuthorInfo = re.compile(r'<a href="oneauthor\.php\?authorid=(?P<id>.*?)" target="_blank">(?P<name>.*?)</a>')
findNovelInfo = re.compile(
    r'<a href="onebook\.php\?novelid=(?P<id>.*?)" target="_blank" title="简介：(?P<intro>.*?)\n标签：(?P<tag>.*?)>(?P<title>.*?)</a>')
findType = re.compile(
    r'<td align="center">\n\s*([\u4E00-\u9FA5]*-[\u4E00-\u9FA5]*-[\u4E00-\u9FA5]*-[\u4E00-\u9FA5]*?)\s*</td>')
findCC = re.compile(r'<td align="center">\n[^\u4E00-\u9FA5]*([\u4E00-\u9FA5]*?)[^\u4E00-\u9FA5]*</td>')
findNums = re.compile(r'<td align="right">([0-9]+?)</td>')
findTime = re.compile(r'<td align="center">([0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+?)</td>\n</tr>')
# 签约状态
# findContractStatus = re.compile(r'<li><span>签约状态：</span><b><font color=\'grey\'>(?P<contractStatus>.*?)</font></b></li>')
# 收藏数
findFavoritesNumber = re.compile(r'<span itemprop="collectedCount">(?P<favoritesNumber>.*?)</span>')