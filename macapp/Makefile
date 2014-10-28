# Create an applicaiton bundle and pack it in a zip file
APP = HumbleCalc.app
ZIP = HumbleCalc.zip

all: zip

zip: app
	zip -r9 $(ZIP) $(APP)

app:
	mkdir -p $(APP)/Contents/MacOS
	mkdir -p $(APP)/Resources
	cp humblecalc.py $(APP)/Contents/MacOS
	cp humblecalc.ico $(APP)/Resources
	cp Info.plist $(APP)/Contents

clean:
	rm -fr $(APP)
	rm -f $(ZIP)

fresh: clean all

.PHONY: all app clean fresh
