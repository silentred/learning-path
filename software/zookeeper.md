# zookeeper

## 选举master的用法

### 步骤：

在确保zookeeper集群节点安装配置的前提下，假设zk已经对外提供了正常的服务，通过下面的步骤来实现Master竞选

1. Client连接到zk上，判断znode /Roles/workers是否存在， 不存在则建立， znode的类型是PERSISTENT类型，保证不会随着C1的session断开而消失。

2. Client在/Roles/workers下面建立一个SEQUENCE|EPHEMERAL类型的znode，前缀可以是worker，由zk保证znode编号是递增而且是暂时的，EPHEMERAL在前文说了，一旦session断开创建的znode也会消失。

3. Client通过getChildren获取所有的/Roles/workers下znode列表，并且设置一个Watcher等待通知，返回值有多少个znode数量就对应Client来竞选。

4. 对于步骤3返回的节点列表进行排序，找到最小的worker编号，如果是和自己创建的一致（步骤2返回值），那么就代表自己的编号是最小的，自己就是Master。如果发现自己的编号不是最小，那么就等待通知，一旦Watcher触发，就在Watcher回到步骤3。

### 上面的机制主要利用了zk的几个特性

1. 对于N个客户端同时请求create一个znode，zk能保证顺序的一致性，并且保证每个客户端创建的znode节点是递增并且唯一。

2. 因为创建的znode是临时的，一旦session断开，那么znode就会从zk上消失，从而给每个设置Watcher的客户端发送通知，让每个客户端重新竞选Master，编号小的肯定是Master，保证了唯一性。



## 分布式写锁

1. create一个PERSISTENT类型的znode，/Locks/write_lock

2. 客户端创建SEQUENCE|EPHEMERAL类型的znode，名字是lockid开头，创建的znode是/Locks/write_lock/lockid0000000001

3. 调用getChildren()不要设置Watcher获取/Locks/write_lock下的znode列表

4. 判断自己步骤2创建znode是不是znode列表中最小的一个，如果是就代表获得了锁，如果不是往下走

5. 调用exists()判断步骤2自己创建的节点编号小1的znode节点(也就是获取的znode节点列表中最小的znode)， 并且设置Watcher， 如果exists()返回false，执行步骤3

6. 如果exists()返回true,那么等待zk通知，从而在回掉函数里返回执行步骤3

释放锁就是删除znode节点或者断开连接就行

*注意：上面步骤2中getChildren()不设置Watcher的原因是，防止羊群效应，如果getChildren()设置了Watcher，那么集群一抖动都会收到通知。在整个分布式锁的竞争过程中，大量重复运行，并且绝大多数的运行结果都是判断出自己并非是序号最小的节点，从而继续等待下一次通知—，这个显然看起来不怎么科学。客户端无端的接受到过多的和自己不相关的事件通知，这如果在集群规模大的时候，会对Server造成很大的性能影响，并且如果一旦同一时间有多个节点的客户端断开连接，这个时候，服务器就会像其余客户端发送大量的事件通知——这就是所谓的羊群效应。


## 全局配置同步

配置文件同步到:zk_agent实现逻辑：
* 初始化连接到zk service，首先竞选出master
* master create一个配置文件管理的PERSISTENT类型的znode，比如是/Applications/NginxConf，
* 启动一个线程，专门接收trigger发送的指令，一收到指令，就create一个"conf-"开头的SEQUENCE|PERSISTENT类型的节点，指定znode数据内容是从trigger收到的数据
* 第一次刚更新会创建节点/Applications/NginxConf/conf-0000000000,以后每次更新新的配置文件编号就会增大。
vim zk_agent.py

配置文件接收应用:zk_appzk_app逻辑如下，它工作在每台worker上
初始化连接到zk service
获取所有/Applications/NginxConf的znode列表并且设置Watcher
找到列表中最大的znode节点，记录它的编号，然后getData获取它的数据，这里就拿到了最新的配置信息
每次又Watcher被触发，就获取列表中编号最大的节点，然后把上一次保存的编号和它比较，一旦又更新就重新获取数据，应用到worker，如果相同就不需要到zk上获取数据。
vim zk_app.py


## zk中watcher单次触发问题

zk中的Watch是一次触发的，一次变更只会触发一个通知，要想下次还得到通知，就需要重新注册。为什么不是永久注册Watcher呢？这主要是考虑到性能上面的影响吧。看下面的情况

1. Client C1对于znode /Task 设置了一个watcher
2. Client C2来到然后对 /Task 增加znode
3. Client C1接收到了notifications，得知监控的znode变化了
4. Client C1在处理这个notifications，这时候Client C3又增加 /task 一个znode

在步骤3的时候C1已经触发了一次watcher，步骤四的时候没有watcher了，除非重新设置watcher，所以这个过过程中就会丢失一个notifications，这就是涉及到了CAP原理了。zookeeper只能保证最终一致性，不能保证强一致性，但是因为zk保证了顺序一致性，所以就能确保最终一致性。

- 强一致性：分布式系统里面一个数据变更后，访问任一个服务都可以得到最新的数据
- 弱一致性：一个数据变更后，其中部分服务可以得到最新数据，部分服务不能
- 最终一致性：在更新某个数据后，可能在开始的时候得不到最新的数据，但是最终是可以呈现最新的数据
- 顺序一致性：更新N份数据，能保证是服务是按照N份数据顺序更新提供服务的。

其实对于上面的case也是有办法解决的，具体就是每次在注册watcher之后都getData，保证数据版本是最新的，但相比较传统的polling优势还是很明显的。


## zk中Versions

每个znode一旦数据变化，都会有一个递增的版本号，在zk API执行的时候都需要指定版本号，客户端提供的版本号只有和服务端匹配了才能进行znode操作。在多个客户端都要操作同一个znode的时候版本号就很重要了。看下面的情况。

1. 比如Client C1写了一个znode /Nginx/conf的数据，写了一些配置信息，这时候/Nginx/conf版本号就从version1变成version2

2. 在上面的同时，Client C2也想写/Nginx/conf，因为C2的客户端版本还是version1，而服务端已经是version2了，此刻就会冲突，这个操作就会以失败告终。所以必须要先更新C2上到version2，然后再提交操作。

3. zk上更新version2到version3，C2本地更新至version3


## zookeeper解决了哪些问题

分布式系统的运行是很复杂的，因为涉及到了网络通信还有节点失效等不可控的情况。下面介绍在最传统的master-workers模型，主要可以会遇到什么问题，传统方法是怎么解决以及怎么用zookeeper解决。

### Master节点管理
集群当中最重要的是Master，所以一般都会设置一台Master的Backup。

Backup会定期向Master获取Meta信息并且检测Master的存活性，一旦Master挂了，Backup立马启动，接替Master的工作自己成为Master，分布式的情况多种多样，因为涉及到了网络通信的抖动，针对下面的情况:
Backup检测Master存活性传统的就是定期发包，一旦一定时间段内没有收到响应就判定Master Down了，于是Backup就启动，如果Master其实是没有down，Backup收不到响应或者收到响应延迟的原因是因为网络阻塞的问题呢？Backup也启动了，这时候集群里就有了两个Master，很有可能部分workers汇报给Master，另一部分workers汇报给后来启动的Backup，这下子服务就全乱了。
Backup是定期同步Master中的meta信息，所以总是滞后的，一旦Master挂了，Backup的信息必然是老的，很有可能会影响集群运行状态。
解决问题:
Master节点高可用，并且保证唯一。
Meta信息的及时同步

### zookeeper Master选举

zookeeper会分配给注册到它上面的客户端一个编号，并且zk自己会保证这个编号的唯一性和递增性，N多机器中只需选出编号最小的Client作为Master就行，并且保证这些机器的都维护一个一样的meta信息视图，一旦Master挂了，那么这N机器中编号最小的胜任Master，Meta信息是一致的。

### 配置文件管理

集群中配置文件的更新和同步是很频繁的，传统的配置文件分发都是需要把配置文件数据分发到每台worker上，然后进行worker的reload，这种方式是最笨的方式，结构很难维护，因为如果集群当中有可能很多种应用的配置文件要同步，而且效率很低，集群规模一大负载很高。还有一种就是每次更新把配置文件单独保存到一个数据库里面，然后worker端定期pull数据，这种方式就是数据及时性得不到同步。

解决问题:
统一配置文件分发并且及时让worker生效

zookeeper发布与订阅模型
发布与订阅模型，即所谓的配置中心，顾名思义就是发布者将数据发布到ZK节点上，供订阅者动态获取数据，实现配置信息的集中式管理和动态更新。例如全局的配置信息，服务式服务框架的服务地址列表等就非常适合使用。

### 分布式锁

在一台机器上要多个进程或者多个线程操作同一资源比较简单，因为可以有大量的状态信息或者日志信息提供保证，比如两个A和B进程同时写一个文件，加锁就可以实现。但是分布式系统怎么办？需要一个三方的分配锁的机制，几百台worker都对同一个网络中的文件写操作，怎么协同？还有怎么保证高效的运行？
解决问题:
高效分布式的分布式锁

zookeeper分布式锁

分布式锁主要得益于ZooKeeper为我们保证了数据的强一致性，zookeeper的znode节点创建的唯一性和递增性能保证所有来抢锁的worker的原子性。

### 集群worker管理

集群中的worker挂了是很可能的，一旦workerA挂了，如果存在其余的workers互相之间需要通信，那么workers必须尽快更新自己的hosts列表，把挂了的worker剔除，从而不在和它通信，而Master要做的是把挂了worker上的作业调度到其他的worker上。同样的，这台worker重新恢复正常了，要通知其他的workers更新hosts列表。传统的作法都是有专门的监控系统，通过不断去发心跳包(比如ping)来发现worker是否alive，缺陷就是及时性问题，不能应用于在线率要求较高的场景
解决问题:
集群worker监控

### zookeeper监控集群

利用zookeeper建立znode的强一致性，可以用于那种对集群中机器状态，机器在线率有较高要求的场景，能够快速对集群中机器变化作出响应。


