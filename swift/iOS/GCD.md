# Grand Central Dispatch

## Serial Queues and Concurrent Queues

Tasks in serial queues execute one at a time, each task starting only after the preceding task has finished.

Tasks in concurrent queues are guaranteed to start in the order they were added. They could finish in different order. 
The decision of when to start a task is entirely up to GCD. If the execution time of one task overlaps with another, it’s up to GCD to determine if it should run on a different core, if one is available, or instead to perform a context switch to a different task.

## Five Queue Types
the main queue, four global dispatch queues

### Main Queue 
is the `only` thread allowed to update your UI.

### Quality of Service (QoS) class
are meant to express the intent of the submitted task so that GCD can determine how to best prioritize it

#### QOS_CLASS_USER_INTERACTIVE
The user interactive class represents tasks that need to be `done immediately` in order to provide a nice user experience. Use it for `UI updates`, `event handling` and `small workloads` that require low latency. The `total amount of work` done in this class during the execution of your app `should be small`.

#### QOS_CLASS_USER_INITIATED
represents tasks that are initiated from the UI and can be performed asynchronously. It should be used when the user is waiting for immediate results, and for tasks required to continue user interaction.

#### QOS_CLASS_UTILITY
represents `long-running tasks`, typically with a user-visible progress indicator. Use it for `computations`, `I/O`, `networking`, continous data feeds and similar tasks. This class is designed to be `energy efficient`.

#### QOS_CLASS_BACKGROUND
represents tasks that the user is not directly aware of. Use it for prefetching, maintenance, and other tasks that don’t require user interaction and `aren’t time-sensitive`.

### 获取这五种队列可以用 只读计算变量

```swift
var GlobalMainQueue: dispatch_queue_t {
  return dispatch_get_main_queue()
}
 
var GlobalUserInteractiveQueue: dispatch_queue_t {
  return dispatch_get_global_queue(Int(QOS_CLASS_USER_INTERACTIVE.value), 0)
}
```

```swift
//调用
dispatch_async(GlobalUserInitiatedQueue) {
  let overlayImage = self.faceOverlayImageFromImage(self.image)
  dispatch_async(GlobalMainQueue) {
    self.fadeInNewImage(overlayImage)
  }
}
```

### Delaying Work with dispatch_after
延时操作

```swift
func showOrHideNavPrompt() {
  let delayInSeconds = 1.0
  let popTime = dispatch_time(DISPATCH_TIME_NOW, Int64(delayInSeconds * Double(NSEC_PER_SEC))) // 1
  dispatch_after(popTime, GlobalMainQueue) { // 2
    let count = PhotoManager.sharedManager.photos.count
    if count > 0 {
      self.navigationItem.prompt = nil
    } else {
      self.navigationItem.prompt = "Add photos with faces to Googlyify them!"
    }
  }
}
```

## Singletons and Thread Safety

```
class FGSingleton {
    static let sharedInstance = FGSingleton()
}
```
关于 dispatch_once, 参考：
http://stackoverflow.com/questions/24024549/dispatch-once-singleton-model-in-swift

### dispatch barriers
create read/write lock to solve Readers-Writers Problem

```swift
private let concurrentPhotoQueue = dispatch_queue_create("com.raywenderlich.GooglyPuff.photoQueue", DISPATCH_QUEUE_CONCURRENT)

var photos: [Photo] {
  var photosCopy: [Photo]!
  dispatch_sync(concurrentPhotoQueue) { // 1
    photosCopy = self._photos // 2
  }
  return photosCopy
}

func addPhoto(photo: Photo) {
  dispatch_barrier_async(concurrentPhotoQueue) { // 1
    self._photos.append(photo) // 2
    dispatch_async(GlobalMainQueue) { // 3
      self.postContentAddedNotification()
    }
  }
}
//2. This is the actual code which adds the object to the array. Since it’s a barrier closure, this closure will never run simultaneously with any other closure in concurrentPhotoQueue.
```


