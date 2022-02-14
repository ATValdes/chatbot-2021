class logSave:

    def __init__(self, fileName):
        self.file = fileName
        with open(fileName,'w') as f:
            pass


    def save(self, message):
        with open (self.file, 'a') as log:
            log.write(message+"\n")

    def show(self):
        with open(self.file, 'r') as log:
            allLines = log.read()
            print(allLines)
            return(allLines)