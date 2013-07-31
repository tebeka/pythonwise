#!/usr/bin/osascript

-- Run ipython on a new iTerm (OS X version)
-- See http://www.iterm2.com/#/section/documentation/scripting

tell application "iTerm"
    activate
    set ipyterm to (make new terminal)
    tell ipyterm
        set ipysession to (make new session)
        tell ipysession
            set name to "IPython"
            exec command "/opt/local/bin/ipython"
        end tell
    end tell
end tell


