# Transform

[UIView transform](http://www.informit.com/articles/article.aspx?p=1951182)

## About `animateWithDuration`
是`class func`, 所以应该这样调用`UIView.animateWithDuration()`。 参数 animations 是 参数为空，返回为Void 的 闭包，在闭包中设置元素的最终状态, 会发生一个从当前状态到最终状态的动画。

## layer
如果想要 rotate around one ceren point, 可以看一下 uiview.layer.anchorPoint

[one answer](http://stackoverflow.com/questions/8275882/one-step-affine-transform-for-rotation-around-a-point)
