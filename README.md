## The problem
If you have ever tried to search for a pypi repo with the 'pip search \<query\>' command you surely got your eyes strained and your heart broken because it's an ugly mess which we shouldn't stand anymore!
## The solution
I created this little helper around pip to approach a friendlier and more beautiful way of searching for python packages.
## See it in action
![yip in action](http://i.imgur.com/P0ezTl5.gif)
## Usage
```
yip search <query>
```
 - searches for packages in the pypi repository that matches the query
 - list them with numbers next to them
 - you type in the number of the package you want to install and hit enter
```
yip list
```
 - lists all python packages installed on your system
```
yip list <query>
```
 - lists installed packages that match the query

## Requirements
Python 3 and pip
 
## Other
 - License can be found in LICENSE.txt
 - Suggestions and pull requests are very welcome! :)
 - If you encounter any bug or have any questions you can post it here or send an e-mail to balazs.saros@gmail.com
