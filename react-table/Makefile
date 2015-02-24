ver=react-0.12.2
zip=$(ver).zip

fetch:
	curl -LO http://facebook.github.io/react/downloads/$(zip)
	unzip $(zip)


server:
	go run httpd.go
