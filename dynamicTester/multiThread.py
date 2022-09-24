import logging
import time
from threading import Thread

def methodOne():
    while True:
        logging.debug("methodOne")
        time.sleep(1)
        logging.debug("methodOne2")
    
def methodTwo():
    while True:
        logging.debug("methodTwo")
        time.sleep(3)
        logging.debug("methodTwo2")
        
def methodThree():
    while True:
        logging.debug("methodThree")
        time.sleep(4)
        logging.debug("methodThree2")
    

def multiThread():
    logging.debug("multiThread")
    threadlist = []
    threadlist.append(Thread(target=methodOne))
    threadlist.append(Thread(target=methodTwo))
    threadlist.append(Thread(target=methodThree))
    
    for t in threadlist:
        t.start()

    for t in threadlist:
        t.join()
    
    logging.debug("HELP")
    return

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    multiThread()
