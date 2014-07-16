httpd: httpd.go image.go
	go build -o $@

clean:
	rm -f httpd
	rm -f image.go


fresh: clean httpd


image.go: image.png
	echo 'package main' > $@
	echo 'var image = []byte{' >> $@
	xxd -i $< | egrep '^[[:space:]]*0x' | sed 's/[^,]$$/,/' >> $@
	echo '}' >> $@
	go fmt $@


.PHONY: test clean fresh
