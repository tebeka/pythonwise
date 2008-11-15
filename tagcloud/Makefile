all: cloud.html

cloud.html: tagcloud.cgi tagcloud.mako
	./tagcloud.cgi | grep -v 'Content-Type' > cloud.html

clean: 
	rm cloud.html

fresh: clean all

.PHONY: all clean fresh
