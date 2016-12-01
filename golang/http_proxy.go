package main

import (
	"flag"
	"fmt"
	"net/http"
	"net/http/httputil"
	"net/url"
)

// our RerverseProxy object
type Prox struct {
	// target url of reverse proxy
	target *url.URL
	// instance of Go ReverseProxy thatwill do the job for us
	proxy *httputil.ReverseProxy
}

// small factory
func newProxy(target string) *Prox {
	url, _ := url.Parse(target)
	// you should handle error on parsing
	return &Prox{target: url, proxy: httputil.NewSingleHostReverseProxy(url)}
}

func (p *Prox) handle(w http.ResponseWriter, r *http.Request) {
	//w.Header().Set("X-GoProxy", "GoProxy")
	r.Host = p.target.Host
	//r.Write(os.Stdout)

	// call to magic method from ReverseProxy object
	p.proxy.ServeHTTP(w, r)
}

// come constants and usage helper
const (
	defaultPort   = ":8080"
	defaultTarget = "http://baidu.com"
)

func main() {
	// flags
	port := flag.String("port", defaultPort, "default server port, ':8080'...")
	url := flag.String("url", defaultTarget, "default redirect url, 'http://baidu.com'")

	flag.Parse()

	fmt.Printf("server will run on %s \n", *port)
	fmt.Printf("redirecting to %s \n", *url)

	// proxy
	proxy := newProxy(*url)

	// server
	http.HandleFunc("/", proxy.handle)
	err := http.ListenAndServe(*port, nil)
	if err != nil {
		panic(err)
	}
}
