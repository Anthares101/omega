<img alt="GitHub" src="https://img.shields.io/badge/version-v1.1-blue"> <img alt="GitHub" src="https://img.shields.io/github/license/anthares101/omega">

# Omega - From Wordpress admin to shell

This tool is to automate the process of getting a shell once you got admin credentials in a Wordpress site. Keep in mind that right now Omega only can attack Linux hosts.

![Omega getting a shell to a Wordpress host](assets/demo.gif)

## How does it work?

First Omega get an admin session in the Wordpress site and using web scrapping, it extracts the current template used by wordpress. After that, it will use the template editor to inject a simple web shell.

Once everything is set up, Omega will spin up a listenner, execute a reverse shell using the web shell injected and wait for the shell to connect back before giving the control the user.

The shell can be stabilize without problems using any method (I hope at least :D).

## Requirements

You need Python 3 installed in your system and also some dependencies that can be installed executing:

```bash
pip3 install -r requirements.txt
```

You can use a virtual env to install the dependencies or intall them system wide.

## Usage

If you have all the requirements you can start playing with Omega! You can add the repository folder to your `PATH` and execute the tool everywhere.

```
Omega - From Wordpress admin to shell

usage: omega.py [-h] -u WP_URL -l USERNAME -p PASSWORD -H LHOST [-P LPORT]

Provides a reverse shell to a Wordpress host (You need an admin credentials!)

optional arguments:
  -h, --help            show this help message and exit
  -u WP_URL, --wp-url WP_URL
                        The target Wordpress url
  -l USERNAME, --username USERNAME
                        Wordpress admin user to use for login
  -p PASSWORD, --password PASSWORD
                        Wordpress admin password to use for login
  -H LHOST, --lhost LHOST
                        The ip where the reverse shell should connect to
  -P LPORT, --lport LPORT
                        The port used to listen for the reverse shell (Default: 8080)
```
