import sys, time, subprocess, signal

def main():
    """try:
        name = sys.argv[1]
    except:
        print 'No player name given!'
        sys.exit()"""
            
    print 'Launcher: Starting name server...'
    ns = subprocess.Popen('pyro-ns')
    print 'Launcher: Name server started with pid:', ns.pid
    time.sleep(5)
    print 'Launcher: Starting application server...'
    server = subprocess.Popen(['python', 'jeopardyclient.py'])
    server.wait()
    ns.send_signal(signal.SIGTERM)
    print 'Launcher: Stopping name server...'
    ns.send_signal(signal.SIGTERM)
    
if __name__ == '__main__':
    main()
