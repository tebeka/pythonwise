#!/bin/bash
# Print messge in the middle of the screen

# Print in middle of screen
msg="Let's boogie, Mr Swine"
offset=$((($(tput cols) - ${#msg})/2))
printf "\n\n\n\n%*s%s\n\n\n\n" ${offset} ' ' "${msg}"
