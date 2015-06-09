## TDD

### PHPUnit

    $someObject = new SomeClass();
    // With PHPUnit
    $phpunitMock = $this->getMock('AClassToBeMocked');
    $phpunitMock->expects($this->once())->method('someMethod');
    // Exercise for PHPUnit
    $someObject->doSomething($phpunitMock);

局限：这里的AClassToBeMocked必须先被创建，而且必须有someMethod这个方法，
才能运行。如果你使用top-down design，就必须实现创建好所有的Class。
这就非常不方便。
[原文链接](http://code.tutsplus.com/tutorials/mockery-a-better-way--net-28097)

### Mockery

    // With Mockery
    $mockeryMock = \Mockery::mock('AnInexistentClass');
    $mockeryMock->shouldReceive('someMethod')->once();
    // Exercise for Mockery
    $someObject->doSomething($mockeryMock);

相对的，Mockery不需要事先创建好所有的Class。
[入门文章](http://www.sitepoint.com/mock-test-dependencies-mockery/)
