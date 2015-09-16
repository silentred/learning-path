# AppCoda Notes

## Auto Layout (Constraints)
Constraints可以用于解决屏幕尺寸带来的布局问题，例如`居中`, 靠边几个points

## UITableView

### Radius Corner

```swift
image.layer.cornerRadius = image.frame.width/2
image.clipsToBounds = true
```
除了在code中定义，还可以用`User Defined Runtime Attributes`, 下文介绍。

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

checkbox `Hide Bars on Swipe`, in Attributes section of NavigationController. 这是全局的设置，所有的NavigationBar都会隐藏。
如果只想某个scene的Bar隐藏，用`navigationController?.hidesBarsOnSwipe = true`. 不能放在 viewDidLoad() 里，因为 viewDidLoad() 只在第一次加载view的时候运行一次。
有两个方法是view每次展现都会调用的方法，`viewWillAppear()`, `viewDidAppear()`, 所以我们可以在其中一个方法里面toggle `hidesBarsOnSwipe`属性，使得不同的scene中NavigationBar 隐藏或者显示。

### Status Bar Style

- First method: 

```swift
override func preferredStatusBarStyle() -> UIStatusBarStyle {
     return .LightContent
}
```
in any ViewController.

- Second method:

Add and set `View controller-based status bar appearance` to `NO` in Project Navigator, under info tab.
Add `UIApplication.sharedApplication().statusBarStyle = .LightContent` to `application(_:didFinishLaunchingWithOptions:)`

Problem: with second methed, there are messages coming out of Debug log, saying "<Error>: CGContextSaveGState: invalid context 0x0. If you want to see the backtrace, please set CG\_CONTEXT\_SHOW\_BACKTRACE environmental variable."  It maybe caused by a bug in xcode, according to google.


## Self Sizing Cell

cell height需要依赖auto layout, 例如垂直居中（上下margin constraint设为0）等。label -> line 默认为1，要设为0，表示自动判断行数.
最后`viewDidLoad()`中设置属性

```swift
self.tableView.estimatedRowHeight = 36.0
self.tableView.rowHeight = UITableViewAutomaticDimension
```

## Basic Animation and Effects

### add toolbar
Toolbar, Bar Button Item. `Bar Button`中的`System Item`可以有很多种选择，有自带的图标。
Button左右可以加上`Flexable Space Bar Button Item`, 用于控制margin.

### set button background as image
如果想改图标的颜色，可以设置`Tint`, 注意要把图片的`Type`设置为`System`, 默认为`Custom`

### Another way to make round corner button
Select a button, in Attribute Inspector, find `User Defined Runtime Attributes`. Add a key named `layer.cornerRadius`, set type as `Number`, value as 32 which is half of the button's width.

### Create a unwind segue
需要在dstController中加一个方法，用来告知系统，这个controller可以被`unwound`, 方法名可以随意定义，但参数和`@IBAction`必须确定。

```swift
@IBAction func close(segue:UIStoryboardSegue){}
```

### Image Blurring Effect
In `viewDidLoad()`, add the following

```swift
let blurEffect = UIBlurEffect(style: UIBlurEffectStyle.Dark)
let blurEffectView = UIVisualEffectView(effect: blurEffect)
blurEffectView.frame = self.view.bounds
blurEffectView.autoresizingMask = [.FlexibleWidth, .FlexibleHeight]
self.backImage.addSubview(blurEffectView)
```

### Animation

in `viewDidiLoad`, predefine the offset position(start status) of buttons. In `viewDidApprear`, set the final status of each button, which is in the `animation` closure. `UIView.animateWithDuration()` can set the time, delay, options...of the animation.

```swift
override func viewDidLoad() {
    // animation
    
    self.fbBtn.transform = CGAffineTransformMakeTranslation(0, 500)
    self.twBtn.transform = CGAffineTransformMakeTranslation(0, -500)
    
    self.msgBtn.transform = CGAffineTransformMakeTranslation(0, 500)
    self.emailBtn.transform = CGAffineTransformMakeTranslation(0, -500)
    
    // background image blurring effect
    let blurEffect = UIBlurEffect(style: UIBlurEffectStyle.Dark)
    let blurEffectView = UIVisualEffectView(effect: blurEffect)
    blurEffectView.frame = self.view.bounds
    blurEffectView.autoresizingMask = [.FlexibleWidth, .FlexibleHeight]
    self.backImage.addSubview(blurEffectView)
    
    super.viewDidLoad()
    
    // Do any additional setup after loading the view.
    
}

override func viewDidAppear(animated: Bool) {
    let offset:CGFloat = 30
    // animation
    UIView.animateWithDuration(0.7, delay: 0.0, options: [], animations: {
            ()->Void in
            self.fbBtn.transform = CGAffineTransformMakeTranslation(0, offset)
            self.emailBtn.transform = CGAffineTransformMakeTranslation(0, -1*offset)
        }, completion: nil)
    
    UIView.animateWithDuration(0.7, delay: 0.3, options: [], animations: {
        ()->Void in
        self.msgBtn.transform = CGAffineTransformMakeTranslation(0, offset)
        self.twBtn.transform = CGAffineTransformMakeTranslation(0, -1*offset)
        }, completion: nil)
    
    UIView.animateWithDuration(0.3, delay: 1, options: [], animations: {
        ()->Void in
        self.msgBtn.transform = CGAffineTransformMakeTranslation(0, 0)
        self.twBtn.transform = CGAffineTransformMakeTranslation(0, 0)
        self.fbBtn.transform = CGAffineTransformMakeTranslation(0, 0)
        self.emailBtn.transform = CGAffineTransformMakeTranslation(0, 0)
        }, completion: nil)
    
}
```

组合动画

```swift
// combined
let scale = CGAffineTransformMakeScale(1, 1)
let translation = CGAffineTransformMakeTranslation(0, 0)
self.dialogVIew.transform = CGAffineTransformConcat(scale, translation)
```

## Map

drag a `MapView` to a new `ViewController`. Import `MapKit`.
Use Segue to pass the address info to the MapViewController. Use `CLGeocoder` to do forward-geocoding to get coordinate of location. 

In `viewDidLoad()`:

```swift
let geoCoder = CLGeocoder()
//print(self.restaurant.location!)
geoCoder.geocodeAddressString(self.restaurant.location!, completionHandler: {
    placemarks, error in
    if error != nil {
        print(error)
        return
    }
    if placemarks != nil && placemarks!.count > 0 {
        
//                for var i=0; i<placemarks!.count ; i++ {
//                    print(placemarks![i].location!.coordinate.longitude)
//                }
        
        let placemark = placemarks![0] as CLPlacemark
        // Add Annotation
        let annotation = MKPointAnnotation()
        annotation.title = self.restaurant.name
        annotation.subtitle = self.restaurant.type
        annotation.coordinate = placemark.location!.coordinate
        self.mapView.showAnnotations([annotation], animated: true)
        self.mapView.selectAnnotation(annotation, animated: true)
    }
})

```

### Show thumbnail of pic on map

`MKMapViewDelegate`, `mapView.delegate = self;`, implement `func mapView(mapView: MKMapView!, viewForAnnotation annotation: MKAnnotation!) -> MKAnnotationView!` to show the AnnotationView on map pin

```swift
func mapView(mapView: MKMapView!, viewForAnnotation annotation: MKAnnotation!) -> MKAnnotationView! {
    let identifier = "MyPin"

    if annotation.isKindOfClass(MKUserLocation) {
        return nil
    }
        // Reuse the annotation if possible
    var annotationView = mapView.dequeueReusableAnnotationViewWithIdentifier(identifier)

    if annotationView == nil {
        annotationView = MKAnnotationView(annotation: annotation, reuseIdentifier: identifier)
        annotationView.canShowCallout = true
    }

    let leftIconView = UIImageView(frame: CGRectMake(0, 0, 53, 53))
    leftIconView.image = UIImage(named: restaurant.image)
    annotationView.leftCalloutAccessoryView = leftIconView

￼   return annotationView
}
```

## Static Table View and Photo Library

In Attribute Inspector -> Content, choose `Static Cells`. So you could set the number of sections and cells in each section.

### picking a photo

Use `UIImagePickerController` to pick image.

Use `UIImagePickerControllerDelegate` and `UINavigationControllerDelegate` to interact with iamge picker interface.

### unwind segue

1. 从按钮或其他obj ctrl+drag 到 exit，则点击按钮时，先`shouldPerformSegueWithIdentifier()`, 再运行`prepareForSegue()`. `should...`方法用于验证是否接着运行 prepareForSegue.

2. 代码启动unwind segue的方法： 从 黄色 controller ctrl+drag 到 exit，创建一个segue. 为其命名 Identifier. 声明 `@IBAction`关联到按钮点击事件。 使用 `performSegueWithIdentifier(identifier, sender)`来启动某个segue

## CoreData

在AppDelegate中配置一个全局的ManagedObjectContext,需要这么几个变量，`applicationDocumentDirectory: NSURL`, 
`managedObjectModel: NSManagedObjectModel`, `persistentStoreCoordinator: NSPersistentStoreCoordinator`, `managedObjectContext: NSManagedObjectContext`

全部用 `lazy var xxx: XXX = { ... return xxx}()` 的方式声明懒加载.

### create Managed Object Model

建完Model, Entity, 选中 Entity，在右侧的 属性栏中要把 Module设为当前项目的名称，否则在调用 `NSEntityDescription.insertNewObjectForEntityForName('Restaurant', inManagedObjectContext: managedObjectContext)` 时会报错。
XCode7之前的版本是在属性栏Class字段写为`SimpleTable.Restaurant`.

### Fetch Data

`NSFetchedResultsController` and Delegate

### Delete Data

### show SQL

`-com.apple.CoreData.SQLDebug`

## Search Bar

## UIPageViewController

## Tab Bar

## UIWebView and MFMailComposeViewController

## CloudKit (not for now)



