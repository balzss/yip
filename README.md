## Intro
If you have ever tried to search PyPI via pip you know how difficult it can be.
Yip is an attempt to resolve that frustration and create a beautiful and feature
rich alternative.
[Here is an article](https://medium.com/@balazs.saros/improving-and-extending-the-search-functionality-of-pythons-pip-50d01a4a344f#.7101f82ei) I wrote about yip on medium.com

## Features
 - **configurable**: every option can be set either explicitly or in a config file
 - **looks better**: with saner result formatting and coloring (which you can turn off)
 - **supports regex**: one of the caveat of pip search is the lack of regex support
 - **more info**: apart from the description it can show you the package size, date of last upload, homepage url or package license
 - **limits results**: want only the 10 most relevant result? No problem!

## Usage example
Normal search:
```
yip <name of package>
```
Normal search with size and license information:
```
yip <name of package> --size --license
```
Regex search with the homepage of the package:
```
yip <regex search query> --regex --homepage
```
Normal search with the 10 most relevant results:
```
yip <name of package> --limit 10
```

## List of flags
```
-h, --help
```
shows information on usage and available flags
```
-d, --date
```
shows the upload date of the latest version
```
-s, --size
```
shows the size in a human readable format
```
-L, --license
```
shows the license of the package
```
-H, --homepage
```
shows the homepage (if has any) of the package
```
-l <number>, --limit <number>
```
limits to the <number> most relevant result
```
-r, --regex
```
allows you to use regex in your search query
*important:* if you use this flag, it will only search in the title, and not in
the summary or in the keyword and you cannot combine it with the -limit flag

## See it in action
*IMPORTANT:* This gif is using the outdated flags which won't work anymore. I
will update it as soon as I can. The usage example/flaglist however updated and
should be used as a reference.
![yip in action](http://i.imgur.com/s56ssMx.gif)

## Config file usage
If you want to make some flags default, automatically sudo install or turn
off the colors you can use a config file for that. You have to create a .yiprc
file in your home directory and paste the example config from this repo. It is
heavily commented and lists all the options you can set. You have to include all
the options or it won't work!

## Requirements
 - *OS-wise:* Developed and tested on Linux however it should work on OSX
 - *software-wise:* Python 3, pip and requests(will switch to xmlrpc, this is
   only temporary)

## Other
 - Licensed under the GPL3
 - Suggestions and pull requests are very welcome! See GitHub's project page for
   TODO-s if you want to contribute. :)
 - If you encounter any bug or have any questions you can post it here or send an e-mail to balazs.saros@gmail.com
