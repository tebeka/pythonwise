httpd: httpd.go image.go
	go build -o $@

clean:
	rm -f httpd
	rm -f image.go


fresh: clean httpd


# Create image byte array using xxd, the sed command adds last comma
image.go: image.png
	echo $<
	echo 'package main' > $@
	echo 'var image = []byte{' >> $@
	xxd -i $< | egrep -i '^[[:space:]]*0x' | sed 's/\([^,]\)$$/\1,/' >> $@
	echo '}' >> $@
	go fmt $@


.PHONY: test clean fresh
