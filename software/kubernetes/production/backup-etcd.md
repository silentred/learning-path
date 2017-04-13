I'm using a bash script from CoreOS team, with small adjustments, that works pretty good. I'm using it more for cluster migration, but at some level can be used for backups too.

```
for ns in $(kubectl get ns --no-headers | cut -d " " -f1); do
  if { [ "$ns" != "kube-system" ]; }; then
  kubectl --namespace="${ns}" get --export -o=json svc,rc,rs,deployments,cm,secrets,ds,petsets | \
jq '.items[] |
    select(.type!="kubernetes.io/service-account-token") |
    del(
        .spec.clusterIP,
        .metadata.uid,
        .metadata.selfLink,
        .metadata.resourceVersion,
        .metadata.creationTimestamp,
        .metadata.generation,
        .status,
        .spec.template.spec.securityContext,
        .spec.template.spec.dnsPolicy,
        .spec.template.spec.terminationGracePeriodSeconds,
        .spec.template.spec.restartPolicy
    )' >> "./my-cluster.json"
  fi
done
```

In case you need to revocer the state after, you just need to execute kubectl create -f ./my-cluster.json