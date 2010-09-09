import sys, json

class Rules:
    def __init__(self):
        self.banner = ''
        self.numRounds = 0
        self.numCategories = []
        self.numQuestions = []

class RuleLoader:
   def  __init__(self, path):
       try:
           self.rawRules = json.load(open(path))
       except (AttributeError, ValueError, IOError):
           print 'Error has occured while loading rule file', path
           sys.exit()
   def validate():
       self.rules = Rules()
       
       return self.rules

def printUsage():
    print 'Usage: ./ruleloader.py <rule_file.json>'
def main():
    if len(sys.argv) < 2:
        printUsage()
        sys.exit()
        
    r = RuleLoader(sys.argv[1])
    print r.rules
    
if __name__ == '__main__':
    main()
