* 1-先定义配置信息

创建config文件夹，作为一个包使用。新建一个config模块，其中配置不同改的开发环境信息
详细的配置变量的说明，查看官方的文档： [Flask配置变量](https://flask.palletsprojects.com/en/1.1.x/config/)	
通过Flask应用实例中的config进行读取。
app.config

* 2-定义模型

创建models文件夹，作为一个包使用。建立各自的表模块，分别做两件事。创建ORM对象、创建ORM对象的Schema。分别使用到flask_sqlalchemy包和marshmallow_sqlalchemy包。

针对使用包时中的注意实现，与参数说明，查看对应的官方文档。创建的这些对象都是在对应的数据库engine上，所以将sqlalchemy创建数据库
 engine的逻辑分配到一个独立模块（包括后期中，需要独立加载进行和关联Flask APP与数据库初始化操作）。

* 3-构建route,和Response

创建routes文件加，作为一个包使用。通过blueprint分别构建不同的路由的模块（稍后说明），针对不同的逻辑主题。

不同的路由导航到不同的处理方法，返回处理结果。通过make_response以json格式返回。

并create standard response codes and messages

