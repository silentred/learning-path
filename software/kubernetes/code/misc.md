
## 关于 RestartPolicy

Docker 的 RestartPolicy 有哪些选项
no
on-failure
unless-stopped
always

k8s没有使用 docker 的重启策略，而是根据 Pod.Spec.RestartPolicy 来判断是否重启


