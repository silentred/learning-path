## 分布式cron的组件

- scheduler 
调度中心，维护所有任务的执行状态，根据任务的tag决定哪些任务在哪些worker上运行。对节点打tag的方式，可以用于dev测试任务, 只需要预先配置一个dev标签的worker实例，即可在其上测试运行任务代码。
支持 一次性任务 和 定时任务 的调度。
对于失效的worker节点，需要重新调度该节点上的所有在执行任务。
对于非幂等的任务，提供一个简单的kv接口，用于任务的状态记录，便于恢复。
三节点raft维持一致性。（前期可以依赖外部存储，状态中心化）

- worker 
负责执行具体的任务，记录上报任务执行的结果。
记录任务结果，根据配置负责重试。
运行环境需要预先配置，例如安装 Python 解释器，package 等。

- job
定义一个任务，包括执行时间，代码，入参，希望执行的worker(用tag表示), owner信息(用于通知)，等。
入参和代码是组合关系，用于代码复用。例如: 创建租户操作，入参可以是 map[ObRegion]NewTenant
job之间可能有依赖关系，暂时不考虑。

- execution
job + timestamp = execution
表示一次具体的执行，每次执行都需要记录结果

参考文章:
《 Reliable Cron across the Planet 》, Google 
https://queue.acm.org/detail.cfm?id=2745840

