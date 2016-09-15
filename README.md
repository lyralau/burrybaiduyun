# Read Me About Burrybaiduyun
因为百度在去年关闭了百度空间，把里面的全部博文都搬到了百度云的文章里面，然后也没提供搬迁功能，导致现在文章取不出来
现在我学了下python，借鉴了几位作者的代码，希望能实现导出功能，把百度云的文章导出XML格式的文件
主要用来导入网易的LOFTER

https://github.com/cheezer/BaiduBlogTransferer
原作者Michael Xie提供的功能主要是导出纯文字和图片链接到一个txt结果文件里面，提供的替换等功能已经很全了，我主要改了一年后一些百度云相应的变化，把输出结果整合到xml里面，参考网易lofter的导入格式做了转换，经过测试后已经成功导入了

准备工作：

bulid时需要的一些包 request，BeautifulSoup，等

把含有单个文章连接的https://wenzhang.baidu.com 的源代码保存在wenzhang_full.htm 里面，方便脚本读取每行源代码

仅支持linux和mac系统，需要有chrome的cookies支持

在Crawler.py的postdata里面输入自己的百度账号

运行Crawler.py

以上。侵权删。