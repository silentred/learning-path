backend default {
        .host = "127.0.0.1";
        .port = "10080";       
}
acl purge {
       "localhost";
       "127.0.0.1";
}

sub vcl_recv {
       if (req.request == "PURGE") {
               if (!client.ip ~ purge) {
                       error 405 "Not allowed.";
                       return(lookup);
               }
       }

               if (req.request != "GET" && req.request != "HEAD") {
                       return(pipe);
               }
               if (req.url ~ "/.(php|cgi)($|/?)") {
                       return(pass);
               }

               if (req.http.Expect) {
                       return(pipe);
               }

               if (req.http.Authenticate || req.http.Cookie) {
                       return(pass);
               }

               if (req.request == "GET" && req.url ~ "/.(gif|jpg|swf|css|js)$") {
                       return(lookup);

               } 
       else {
               return(lookup);
            }
       }


sub vcl_miss {
       if (req.request == "PURGE") {
               error 404 "Not in cache.";
       }
}

