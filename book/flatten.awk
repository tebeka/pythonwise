# "flatten" multiple files to single one
/INCLUDE/ { system("cat " $2); next}
// { print $0 }
