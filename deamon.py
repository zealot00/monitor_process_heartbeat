#! /usr/bin/env python


import os,sys
import ConfigParser
config = ConfigParser.ConfigParser()


def load_global_config():
    config_file = "/etc/ghost.conf"
    config.readfp(open(config_file))
    try:
            script_enable = config.getboolean('global','enable')
            config_file = config.get('global','logfile')
            pid_file = config.get('global','pidfile')
            interval = int(config.get('global','interval'))
            mail = config.get('global','mail')
            monitor_process = config.get('global','moitorprocess')         
   
             
    except ConfigParser.NoOptionError,e:
        pass
    except ValueError,e:
        print >> sys.stderr, "%s ! config file error! global => enable only 'true' or 'false' !" % e
        sys.exit(1)
    
       
  # sections = config.sections()
  # for section in sections:
  #     option = config.options(section)
  #     print option
   

    


def main():
    import time
    f = open('/tmp/daemon-log','w')
    while 1:
        f.write('%s/n' % time.ctime(time.time()))
        f.flush()
        time.sleep(10)


if __name__ == "__main__":
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError,e:
        print >> sys.stderr, "fork #1 failed: %d(%s)" %(e.errno,e.strerror)
        sys.exit(1)

    os.chdir('/')
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            print "Daemon PID %d" % pid
            sys.exit(0)
    except OSError,e:
        print >> sys.stderr,"fork #2 failed: %d(%s)" % (e.errno,e.strerror)
        sys.exit(1)

    main()
