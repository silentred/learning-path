package main

import (
	"flag"
	"fmt"
	"net/http"
	"os"

	"github.com/labstack/echo"
	"github.com/labstack/gommon/log"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"github.com/silentred/rotator"
)

var (
	host, port string

	reqCount = prometheus.NewCounterVec(prometheus.CounterOpts{
		Name: "req_count",
		Help: "total count of request",
	}, []string{"service"})

	logger echo.Logger
)

func main() {
	flag.StringVar(&host, "host", "", "host usage")
	flag.StringVar(&port, "port", ":9090", "host usage")
	flag.Parse()

	fmt.Println(host, port)
	svcAddr := os.Getenv("HELLO_PORT_9090_TCP")
	prometheus.MustRegister(reqCount)

	initLogger()

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		reqCount.WithLabelValues("http").Add(1)
		logger.Info("test")
		fmt.Fprintf(w, "HostAddr=%s, uri=%s !", svcAddr, r.URL.Path[1:])
	})

	http.Handle("/metrics", promhttp.Handler())

	panic(http.ListenAndServe(port, nil))
}

func initLogger() {
	logger = log.New("hello")
	r := rotator.NewFileSizeRotator("/tmp", "hello-app", "log", 100<<20)
	logger.SetOutput(r)
}
