# PyCC (Python Command & Control)
==============================
<pre>
 ~ Command & Control via Python ~
       .o   .oooooooooo.                 .oooooo.    .oo.    .oooooo. 
      .8'  .8'`888   `Y88.             d8P'  `Y8b .88' `8.  d8P'  `Y8b
  .888888888888888   .d88'oooo    ooo888         88.  .8' 888        
    .8'  .8'   888ooo88P'  `88.  .8' 888         `88.8P   888        
.888888888888' 888          `88..8'  888          d888[.8'888        
  .8'  .8'     888           `888'   `88b    oo  88' `88. `88b    ooo
 .8'  .8'     o888o           .8'     `Y8bood8P' `bodP'`88.`Y8bood8P'
                              o..P'                                         
                             `Y8P'   
               ~ Multi-threaded telnet command execution ~
                      ~ silentphoenix & shellzrus ~
</pre>
===============================

# Usage
<pre>
usage: pycc.py [-h] [-c CMD] [-l HOSTLIST]

optional arguments:
  -h, --help            show this help message and exit
  -t MAXTHREADS, --maxThreads 
                        MAXTHREADS Max threads to allow before bailing
  -c CMD, --cmd CMD     Command to run on the hosts
  -l HOSTLIST, --hostlist HOSTLIST
                        List of hosts to manage
</pre>
# Set up

* Create a file with your telnet hosts, one per line
* Edit your credentials, prompts, etc
* Run it.

# Other Uses

This program is a fine piece of python because you can also use it to handle other programs (like shell scripts, or netcat, etc). Just edit the host_functiom paremeters. Was originally multithreading telnet through expect, until I rewrote it to just use python (to conserve resources and for cleansliness).


