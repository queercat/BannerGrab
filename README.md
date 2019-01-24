# BannerGrab.py
-----------------
A unique and custimizable take on banner grabbing. The big idea is that each port can have custom behaviors such that say...
Port 80 could be setup as: ['HEAD bla bla bla', 'GET bla bla bla', 'POST blablabla'].
And it would cycle through each behavior and log the results.

# Installation
----------------
`git clone https://github.com/queercat/BannerGrab/`
`cd BannerGrab`

# Usage
`python bannergrab.py [hosts] -p --ports -v --verbose -n --no-log`
> example
`python bannergrab.py google.com,wikipedia.com,192.168.1.1 -p 23,25,80 -v`