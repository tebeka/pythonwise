test:
	go test -v

image: state-machine.png

state-machine.png: state-machine.dot
	dot -Tpng -o $@ $<
