[Problem] Go http server reset by peer

https://stackoverflow.com/questions/17714494/golang-http-request-results-in-eof-errors-when-making-multiple-requests-successi/23963271#23963271


I agree with the assertion that you shouldn't be hitting outside servers in your unit tests, why not just use the built-in http.Server and serve up the content that you want to test. (There is actually the httptest package to help with this)

I recently ran into this same problem while trying to crawl sitemaps, and this is what I have found so far:

Go by default will send requests with the header Connection: Keep-Alive and persist connections for re-use. The problem that I ran into is that the server is responding with Connection: Keep-Alive in the response header and then immediately closing the connection.

As a little background as to how go implements connections in this case (you can look at the full code in net/http/transport.go). There are two goroutines, one responsible for writing and one responsible for reading (readLoop and writeLoop) In most circumstances readLoop will detect a close on the socket, and close down the connection. The problem here occurs when you initiate another request before the readLoop actually detects the close, and the EOF that it reads get interpreted as an error for that new request rather than a close that occurred prior to the request.

Given that this is the case the reason why sleeping in between requests works is that it gives readLoop time to detect the close on the connection before your new request and shut it down, so that your new request will initiate a new connection. (And the reason why it would intermittently fail is because there is some amount code running between your requests and depending of scheduling of goroutines, sometimes the EOF will be properly handled before your next request, sometimes not). And the req.Close = true, solution works because it prevents the connection from being re-used.

There is a ticket related to this situation: https://code.google.com/p/go/issues/detail?id=4677 (and a dupe ticket that I created that allowed me to reliably reproduce this: https://code.google.com/p/go/issues/detail?id=8122)