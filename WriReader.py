import threading
import time

data = [[1, 'R', 3, 5],
        [2, 'W', 4, 5],
        [3, 'R', 5, 2],
        [4, 'R', 6, 5],
        [5, 'W', 5.1, 3]]

RP_Write = threading.Lock()
CS_Write = threading.Lock()
CS_Read = threading.Lock()

readCount = 0
lockReadCount = threading.Lock()
writerCount = 0
lockWriterCount = threading.Lock()


class RP_Reader(threading.Thread):
    def __init__(self, threadName, delay, persist):
        super().__init__(name=threadName)
        self.delay = delay
        self.persist = persist

    def run(self):
        global value, lockReadCount, readCount, RP_Write
        time.sleep(self.delay)

        current = time.clock()
        print('%.2f ' % (current - start) + 'Reader thread %s send the reading require.' % self.name)

        lockReadCount.acquire()
        readCount += 1
        if readCount == 1:
            RP_Write.acquire()
        lockReadCount.release()

        current = time.clock()
        print('%.2f ' % (current - start) + 'Reader thread %s began to read file.' % self.name)
        time.sleep(self.persist)
        current = time.clock()
        print('%.2f ' % (current - start) + 'Reader thread %s finished reading file.' % self.name)

        lockReadCount.acquire()
        readCount -= 1
        if readCount == 0:
            RP_Write.release()
        lockReadCount.release()


class RP_Writer(threading.Thread):
    def __init__(self, threadName, delay, persist):
        super().__init__(name=threadName)
        self.delay = delay
        self.persist = persist

    def run(self):
        global value, lockReadCount, readCount, RP_Write
        time.sleep(self.delay)

        current = time.clock()
        print('%.2f ' % (current - start) + 'Writer thread %s send the writing require.' % self.name)

        RP_Write.acquire()

        current = time.clock()
        print('%.2f ' % (current - start) + 'Writer thread %s began to write to the file.' % self.name)
        time.sleep(self.persist)

        current = time.clock()
        print('%.2f ' % (current - start) + 'Writer thread %s finished writing to the file.' % self.name)

        RP_Write.release()


def ReaderPriority():
    global start, readCount, writerCount
    readCount = 0
    writerCount = 0
    start = time.clock()

    print('ReaderPriority:')
    threads = []
    for item in data:
        if item[1] == 'R':
            tmp = RP_Reader(str(item[0]), item[2], item[3])
            tmp.start()
            threads.append(tmp)
        else:
            tmp = RP_Writer(str(item[0]), item[2], item[3])
            tmp.start()
            threads.append(tmp)
    flag = True
    while flag:
        flag = False
        for item in threads:
            flag = flag or item.isAlive()
    print('All reader and writer have finished operating.')


class WP_Reader(threading.Thread):
    def __init__(self, threadName, delay, persist):
        super().__init__(name=threadName)
        self.delay = delay
        self.persist = persist

    def run(self):
        global value, lockReadCount, readCount, CS_Write, writerCount, lockWriterCount
        time.sleep(self.delay)

        current = time.clock()
        print('%.2f ' % (current - start) + 'Reader thread %s send the reading require.' % self.name)

        lockWriterCount.acquire()
        lockWriterCount.release()

        lockReadCount.acquire()
        readCount += 1
        if readCount == 1:
            CS_Read.acquire()
        lockReadCount.release()

        current = time.clock()
        print('%.2f ' % (current - start) + 'Reader thread %s began to read file.' % self.name)

        time.sleep(self.persist)

        current = time.clock()
        print('%.2f ' % (current - start) + 'Reader thread %s finished reading file.' % self.name)

        lockReadCount.acquire()
        readCount -= 1
        if readCount == 0:
            CS_Read.release()
        lockReadCount.release()


class WP_Writer(threading.Thread):
    def __init__(self, threadName, delay, persist):
        super().__init__(name=threadName)
        self.delay = delay
        self.persist = persist

    def run(self):
        global value, lockReadCount, readCount, CS_Write, writerCount, lockWriterCount
        time.sleep(self.delay)

        current = time.clock()
        print('%.2f ' % (current - start) + 'Writer thread %s sent the writing acquire.' % self.name)

        lockWriterCount.acquire()
        writerCount += 1
        if writerCount == 1:
            CS_Read.acquire()
        lockWriterCount.release()

        CS_Write.acquire()

        current = time.clock()
        print('%.2f ' % (current - start) + 'Writer thread %s began to write to the file.' % self.name)
        time.sleep(self.persist)
        current = time.clock()
        print('%.2f ' % (current - start) + 'Writer thread %s finished writing to the file.' % self.name)

        CS_Write.release()

        lockWriterCount.acquire()
        writerCount -= 1
        if writerCount == 0:
            CS_Read.release()
        lockWriterCount.release()


def WriterPriority():
    global start, readCount, writerCount
    readCount = 0
    writerCount = 0
    start = time.clock()

    print('WriterPriority:')
    threads = []
    for item in data:
        if item[1] == 'R':
            tmp = WP_Reader(str(item[0]), item[2], item[3])
            tmp.start()
            threads.append(tmp)
        else:
            tmp = WP_Writer(str(item[0]), item[2], item[3])
            tmp.start()
            threads.append(tmp)
    flag = True
    while (flag):
        flag = False
        for item in threads:
            flag = flag or item.isAlive()
    print('All reader and writer have finished operating.')


start = 0

while True:
    print('1.ReaderPriority\n2.WriterPriority\n3.Exit\nPlease input a number')
    option = 0
    while option != '1' and option != '2' and option != '3':
        option = input()

    if option == '1':
        ReaderPriority()
    elif option == '2':
        WriterPriority()
    else:
        break
