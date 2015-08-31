# AppCoda Notes

## Auto Layout (Constraints)
Constraints可以用于解决屏幕尺寸带来的布局问题，例如`居中`, 靠边几个points

## UITableView

### Radius Corner
UIImage.layer.cornerRadius = UIImage.frame.width/2
UIImage.clipsToBounds = true

### Protocol
`UITableViewDataSource`, `UITableViewDelegate`等。


## UITableViewController

### DataSource Rendering
`override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int`, `override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath)`

`override func numberOfSectionsInTableView(tableView: UITableView) -> Int`, 需要查找Sectiond指代的意义，目前直接返回1.

关于cell的重用，使用`tableView.dequeueReusableCellWithIdentifier`，注意在storyboard中给cell一个 `Identifier`. 

关于将storyboard中的view和代码关联起来，需要在 `custom class` 中设置关联的class name.

### Cell Select Event
`override func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath)`

`UIAlertController`用来构建一个AlertSheet 或者 Alert.使用`addAction`来添加`UIALertAction`(类似Button) . `UIAlertAction`到构造方法中有回调，可以设置点击后执行的代码。
使用 `self.presentViewController`渲染到界面上。

### Delete

`override func tableView(tableView: UITableView, commitEditingStyle editingStyle: UITableViewCellEditingStyle, forRowAtIndexPath indexPath: NSIndexPath)`, 其中有一个switch判断操作类型：

```swift
if editingStyle == .Delete {
    // Delete the row from the data source
} else if editingStyle == .Insert {
    // Create a new instance of the appropriate class, insert it into the array, and add a new row to the table view
    
}    
```

在view中渲染删除的方法：
`tableView.deleteRowsAtIndexPaths` 或者但不推荐`self.tableView.reloadData()`

### Swipe with "More" Action

`override func tableView(tableView: UITableView, editActionsForRowAtIndexPath indexPath: NSIndexPath) -> [UITableViewRowAction]?`
返回`UITableViewRowAction`数组optional, 每个Action代表swipe后出现的一个按钮，可以设置名称，style，回调等。

实现了这个方法后，就不会像之前一样自动生成`Delete`按钮了，所以需要自己创建。

UITableViewRowAction.backgroundColor = UIColor(), UIColor代表颜色

## Navigation Controller

### Add a new NavigationController
storyboard中选中TableViewController, Editor -> Embed In -> Navigation Controller，自动插入了一个Navigation Controller, 并在TableView同级下创建了一个 Navigation Bar. 设置它的title。

### Add a segue to connect Views
In storyboard, 从TableCell Ctrl+Drag 到新建的 ViewController. Segue新建完成。由于Segue会很多，需要给一个Identifier. 

从SourceController触发Segue之后，在动画出现之前，会调用SourceController中的`prepareForSegue()`方法，在此方法中可以传递数据到 DestinationController。在目标ViewContoller中，`viewDidLoad()`方法中把数据渲染到视图。

```swift
override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
    if segue.identifier == "ShowRestDetail" {
        if let indexPath = self.tableView.indexPathForSelectedRow {
            let destinationController = segue.destinationViewController as! DetailViewController
            destinationController.restImage = "restaurant"
            destinationController.restName = self.restaurantNames[indexPath.row]
            //print(indexPath)
        }
    }
}
```

## OOP

## UITableView: Delegate and DataSource
代理类需要实现 `UITableViewDataSource`, `UITableViewDelegate`才能渲染Table. 还需要右键TableView, 把`dataSource`, `delegate`连接到代理类. `UITableViewController`貌似不需要连接，可能是已经连接了父类。

### table appearance
`tableView.backgroundColor`, `tableView.tableFooterView`, `tableView.separatorColor`

### NavigationBar Appearance
在`AppDelegate.swift`中的application方法中全局修改。 `UINavigationBar.appearance().barTintColor`等。

在 `TableViewController`中修改`self.navigationItem.backBarButtonItem = UIBarButtonItem(title: "", style: .Plain, target: nil, action: nil)`，在`DetailView`中显示导航栏中back按钮的效果.

相对的是，在`DetailViewController` 中修改`title`属性，detail视图中导航栏title得到改变。






