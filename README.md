# Storyboard & Xliff Tools
My personal collection of scripts to speed up some tasks in my Xcode development process.

##### *** WARNING: These are small scripts, written in short time, without any coding style and tailor made to my necessities. 



## update_storyboard_base.py

Read trasnslations from a xliff file and update base Localization of a xcode storyboard. 

It's useful when you need to change the base localization language and you don't want to rewrite everything in your storyboard.

**Suggested steps:**

* Export xliff from xcode
* Take the xliff file in the language you want use (or translate it)
* Make a backup of you storyboard
* Change paths in this script and run it
* Replace your storyboard and check it in xcode



## convert_strings_to_nslocalizedstrings.py

Cycle thru .m files (only Objective C, no Swift sorry) and find all strings not yet "NSLocalized" and ask for each strings what to do.
Finally you have modified .m files and a .strings file with your key/string paits

**Suggested steps:**

* Make a backup (also if the script create a backup or each file)
* Change paths in this script and run it
* decide one by one which strings to convert
* Replace your .m files and check it in xcode

**todo**

* avoid duplicate key in .strings file
* implement black list to avoid to elaborate not localisable strings (NSLog, NSLocalizeString, etc etc)