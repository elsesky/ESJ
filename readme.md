# 环境说明

编译环境基于python2.7.18（32位），同理，下面的包如果存在x86_64或x86的区别，务必使用x86版本，且需要对应python2.7版本的包
至少需要以下包
pywin32
requests
py2exe
pyqt4
ConfigParser
MySQLdb

# 使用说明

运行前先记得把esj.ini.tpl改名为esj.ini
然后在esj.ini文件中配置好对应项目

# 关于UI的复制使用说明

## 架构说明

`

/
├─esj_ui.py
├─esj_ui_core.py
└─ui
   ├─Core.py
   ├─uiesj.py
   ├─uiesj.ui
   └─__init__.py
`

## 文件用途及修改说明

### uiesj.ui

该文件为实际使用Qt绘图工具绘制的窗体。
可以通过命令转换为py文件。
注意，转换出来的文件的类名，与窗体名称一致，转换前记得修改窗体名字与文件名一致。

### uiesj.py

为uiesj.ui通过命令转换出来的文件。

### Core.py

窗体实际初始化的文件，里面初始化了主窗口，并定义了窗体启动时执行的初始化任务。
需要注意的代码：

`
from uiesj import *
`

其中的“uiesj”根据前面具体的.ui后缀的文件名称对应。

### __init__.py

整个ui库的初始化，里面定义了要引用的文件，如Core.py和uiesj.py

### esj_ui.py

程序入口文件，直接python调用
该文件中需要注意的部分

`
from esj_ui_core import *
`

这段中esj_ui_core为对应核心文件。
其他内容可以保持不变。

### esj_ui_core.py

该文件用于实现窗体具体功能
该文件用于引用实际的UI窗体库
需要注意以下内容

`
from ui import *
`

这段中的“ui”为ui文件夹名称，用于显式导入整个ui库。
