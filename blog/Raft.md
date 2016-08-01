# Raft

## Overview

## Leader Election

## Log Replication

## Safety

因为当一个server作为follower时，可能会和leader失去通信，当这台server之后被选为leader时，他就没有持有部分log。
raft 和其他协议不同，他保持 log 从 leader -> follower 的单向传输，leader不用覆盖(overwrite)自己的log。（其他例如 Viewstamped Replication 会检测leader缺失哪些log， 并从follower中取）

Raft如何保证每个新的leader都持有上一个leader的全部log entries? 

### Election Restriction

在投票(voting)时，只有拥有全部committed log的节点，才可以被选为 leader. 
Candidate 在竞选时，会和大多数节点通信，每一条committed log至少会存在于这些节点中的某个一个节点上。
Candidate 发起RequestVote RPC时，会把自身的 log带上，如果voter 发现自己的log比较“新”，则会拒绝选这个candidate为leader。
比较谁比较新是通过比较 last entry 的 index 和 term 来实现的.
先比较term: if entryA.term > entryB.term ， 则 A 比较新. (term是选举的轮数)
再比较index: 如果A, B的last entry的term一样，谁的 index 大，谁比较新 (index是随着新插入的entry自增的)

### Committing entry from previous term









