# iOS Development In Swift

## XCode Interface


## Build Basic UI

### Connect UI to Code

### ViewController

### Custom Control

### Data Model

### Test Is Easy


## Table View

### Create a Table View Controller
在`Object Library`中找到Table View Controller, 拖到storyboard. 如果想让其成为 `initial scene`, 只需要拖动`entry point`指向Table View Controller即可。

### Configue 
在storyboard中打开`outline view`, 选择Table View, 在 utility area中打开 `Size Inspecter`(第五个图标), Row Height输入90.

### Design Custom Table Cell
每一行都是由`UITableVIewCell`管理,负责绘制内容。
1. 新建一个Coco Touch Class文件
2. 名称Meal, subclass of `UITableViewCell`, xcode会自动将命名改为`MealTableViewCell`
3. 连接Custom Table Cell到storyboard: 在 outline 中选择Table View -> Tabel View Cell, 
打开 `Attribute Inspecter`(第四个图标), `Identifier`输入`MealTableViewCell`. `Selection`to None, 这样在用户tap的时候不会出现高亮。在Size Inspecter中把Row Height设置为90. 在`Identity Inspecter`中设置`Class`为`MealTableViewCell`
4. 拖动一个ImageView到TableViewCell中，设置defaultPhoto; 拖动一个Label到图片右侧上部，调整大小； 拖动一个View到图片右侧下部，作为StarControl, 可以利用之前写的那个View. 在Identifier中Class设置为StarControl. 在Attributes中，把`User Interaction Enabled`取消。

## Navigation Controller










