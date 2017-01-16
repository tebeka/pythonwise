all: hi

hi: hi.a hi.c
	gcc -pthread -o hi hi.c hi.a

hi.a: hi.go
	go build -buildmode=c-archive -o $@ $<

clean:
	rm -f hi.a
	rm -f hi

fresh: clean all

.PHONY: all clean fresh
