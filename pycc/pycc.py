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
semaphore = threading.Semaphore(50)
prompt = "login: " # < set your prompt
passPrompt = "Password: "
user = "" # < set your credentials
password = ""
# try to pass hosts that cant connect/fail
def connect(host, cmd):
    try:
        tn = telnetlib.Telnet(host)
    except:
        pass
    else:

        try:
            tn.read_until(prompt)
            tn.write(user + "\n")
            if password:
                tn.read_until(passPrompt)
                tn.write(password + "\n") 
            tn.write("%s \n" % cmd) # send command string
            tn.write("exit\n") # exit
            resp = tn.read_all()
            logging.basicConfig(filename='PyCC.log',level=logging.INFO)
            logging.info(resp) # log & print stout/er
            print(resp)
        except EOFError:
            pass
     
def execute(cmd, hostlist, maxThreads):
    print("[*] Maximum of %s threads specified..." % maxThreads)
    threads=[]
    thread_holder = []
    count=0
    tcount=0
    #maxthreads=int(maxthreads)    
    with open(hostlist) as f:
        hostlist=[]
        hostlist=f.readlines()
        for host in hostlist:
            try:
                threading.Thread(target=connect, args=(host,cmd )).start()
            except Exception, e:
                print("[!] Threading Error: %s : Check log for debug info..." % e)
                logging.info(threading.enumerate())
            count+=1
            tcount+=1
            if count>=10:
                #print("[*] %s threads running..." % numThrd)
                activeThreads = (threading.active_count())-1
                print("[*] %s threads running currently..." % activeThreads)
                print("[*] Started %s theads total..." % tcount)
                count=0 # reset count
            if tcount>int(maxThreads):
                break
                print("[*] Bailing because reached max threads (%s)" % maxThreads)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--cmd',default='pwd', help='Command to run on the hosts')
    parser.add_argument('-l','--hostlist',default='lists/default.lst', help='List of hosts to manage')
    parser.add_argument('-t','--maxThreads',default='500', help='Max threads to allow before bailing')
    ns = parser.parse_args()

    cmd = ns.cmd if ns.cmd is not None else "default_cmd"
    hostlist = ns.hostlist if ns.hostlist is not None else "default_list"
    maxThreads = ns.maxThreads if ns.maxThreads is not None else "default_maxThreads"

    try:
        f = open(hostlist, 'r')
    except IOError:
        print ("[!] Cannot open %s, does it exist?" % hostlist)
        sys.exit(1)
    else:
        f.close()

    execute(cmd, hostlist, maxThreads)


if __name__ == '__main__':
    main()
