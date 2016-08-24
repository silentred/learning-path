curl -XPUT http://127.0.0.1:9200/_watcher/watch/error_status -d'
{
    "metadata" : {
        "color" : "red"
    },

    "trigger": {
        "schedule": {"interval" : "10s"}
    },

    "input": {
        "search" : {
            "request":{
                "indices" : [ "ls-api-log-lumen-*"],
                "body" : {
                    "query" : {
                        "filtered" : {
                            "query" : { "match" : { "level" : "error" }},
                            "filter" : { "range" : { "@timestamp" : { "from" : "now-5m" }}}
                        }
                    }
                }
            }
        }
    }

    "condition" : {
        "compare" : { "ctx.payload.hits.total" : { "gt" : 0 }}
    },

    "actions" : {
        "call_slack": {
            "webhook": {
                "method": "POST",
                "host": "localhost",
                "port": 8083,
                "path": "alert",
                "body": "Encountered {{ctx.payload.hits.total}} errors"
            }
        }
    }
}'