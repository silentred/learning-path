# Slider Menu

[SWRevealController](http://www.appcoda.com/sidebar-menu-swift/)

## 代码

## 原理

## 如何实现




# Pull to Refresh

## 原生自带了`UIRefreshControl`

```swift
in viewDidLoad()
refreshControl = UIRefreshControl()
tableView.addSubview(refreshControl)

func scrollViewDidEndDecelerating(scrollView: UIScrollView) {
    if refreshControl.refreshing {
        performSelector("stopRefresh", withObject: self, afterDelay: NSTimeInterval(2.0))
    }
}

func stopRefresh(){
    refreshControl.endRefreshing()
    dataArray.append("new one")
    tableView.reloadData()
}
```

## 第三方库 

### CBStoreHouseRefreshControl
注意需要复制 xxx.plist 到根目录， 里面定义了 loading 几何图形的形状。

有一个问题，在 CBStoreHouseRefreshControl.m 中，

```swift
if (self.originalTopContentInset == 0) self.originalTopContentInset = self.scrollView.contentInset.top;
```
强制为 scrollView 加了 inset, 需要注释掉。

## 如何加在 table footer

## 如何自己实现

