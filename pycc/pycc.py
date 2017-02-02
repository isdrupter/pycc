#!/usr/bin/python
print(
"""
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
""")
import os,sys,threading,time,logging,telnetlib,argparse
file_name = os.path.basename(sys.argv[0])
hostlist = "" # initialize only \
cmd = "" # ,grabbed through argparse
maxThreads = ""
mode = ""
timeout = ""
semaphore = threading.Semaphore(50)
prompt = "ogin: " # < set your prompt
passPrompt = "Password: "
user = "admin" # < set your credentials
password = "password"
# try to pass hosts that cant connect/fail
def connect(host, cmd, mode, timeout):
    timeout = int(timeout)
    logging.info(host)
    try:
        tn = telnetlib.Telnet(host, 23, timeout)
    except:
        pass
    else:
        # connect telnet
        try:
            #tn.readuntil(prompt)
            tn.read_until(b'ogin:', 10)
            tn.write(user + "\n")
            if password:
                #tn.read_until(passPrompt)
                tn.read_until(b'assword:', 10)
                tn.write(password + "\n")
            if mode == "d":
                print("[*] Sending daemonized command to %s ..." % host)
                tn.write("trap '' 1;(%s)>/dev/null 2>&1 & \n" % cmd) # send daemonized command string
            else:
                print("[*] Sending command to %s ..." % host)
                tn.write("%s \n" % cmd) # just send the command
            tn.write("exit\n") # finally send exit
            resp = tn.read_all()
            logging.basicConfig(filename='PyCC.log',level=logging.INFO)
            logging.info(resp) # log & print stout/er
            print(resp)
        except EOFError:
            pass
     
def execute(cmd, hostlist, maxThreads, mode, timeout):
    print("[*] Maximum of %s threads specified..." % maxThreads)
    threads=[]
    count=0
    tcount=0
    #maxthreads=int(maxthreads)    
    with open(hostlist) as f:
        hostlist=[]
        hostlist=f.readlines()
        for host in hostlist:
            try:
                threading.Thread(target=connect, args=(host,cmd,mode,timeout )).start()
            except Exception, e:
                print("[!] Threading Error: %s : Check log for debug info..." % e)
                logging.info(threading.enumerate())
            count+=1
            tcount+=1
            if count>=10:
                #print("[*] %s threads running..." % numThrd)
                activeThreads = (threading.active_count())-1
                print("[*] %s threads running concurrently..." % activeThreads)
                #print("[*] Started %s theads total..." % tcount)
                count=0 # reset count
            if tcount>int(maxThreads):
                break
                print("[*] Bailing because reached max threads (%s)" % maxThreads) # should never actually see this error


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--cmd',default='pwd', help='Command to run on the hosts')
    parser.add_argument('-l','--hostlist',default='lists/default.lst', help='List of hosts to manage')
    parser.add_argument('-t','--maxThreads',default='500', help='Max threads to allow before bailing')
    parser.add_argument('-m','--mode',default='shell', help='Mode: s/d (shell/daemon) Trap and send command to background if daemonize. Defaults to shell')
    parser.add_argument('-T','--timeout',default='60', help='Default telnet timeout Defaults to 60. Increase for longer running commmands. Defaults to 60')
    ns = parser.parse_args()

    cmd = ns.cmd if ns.cmd is not None else "default_cmd"
    hostlist = ns.hostlist if ns.hostlist is not None else "default_list"
    maxThreads = ns.maxThreads if ns.maxThreads is not None else "default_maxThreads"
    mode = ns.mode if ns.mode is not None else "default_mode"
    timeout = ns.timeout if ns.mode is not None else "default_timeout"
    try:
        f = open(hostlist, 'r')
    except IOError:
        print ("[!] Cannot open %s, does it exist?" % hostlist)
        sys.exit(1)
    else:
        f.close()

    execute(cmd, hostlist, maxThreads, mode, timeout)


if __name__ == '__main__':
    main()
