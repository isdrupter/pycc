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
semaphore = threading.Semaphore(50)
prompt = "login: "
passPrompt = "Password: "
user = "username" # credentials
password = "password"

def connect(host, cmd):
    try:
        tn = telnetlib.Telnet(host)
    except:
        pass
    else:
    #if not check: return # test connection
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
     
def execute(cmd, hostlist):
    threads=[]
    thread_holder = []
    count=0
    tcount=0
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
                activeThreads = (threading.active_count())
                print("[*] %s threads running currently..." % activeThreads)
                print("[*] Started %s theads total..." % tcount)
                count=0
             if tcount>=5000:
                break
                print("[!] 5000 Threads! Bailing!!!")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--cmd',default='ifconfig eth1', help='Command to run on the hosts')
    parser.add_argument('-l','--hostlist',default='lists/default.lst', help='List of hosts to manage')
    ns = parser.parse_args()

    cmd = ns.cmd if ns.cmd is not None else "default_cmd"
    hostlist = ns.hostlist if ns.hostlist is not None else "default_list"
    
    execute(cmd, hostlist)



if __name__ == '__main__':
    main()
