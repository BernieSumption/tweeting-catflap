import sys, random

def die(message):
    print >> sys.stderr, "Error:", message
    exit(1)

class Grammar(object):

    _lines = []
    nodes = {}
    
    def add_node_option(self, node, fragment):
        if not node in self.nodes:
            self.nodes[node] = []
        self.nodes[node].append(fragment)
    
    def generate(self):
        if not "__root__" in self.nodes:
            die("no tweets are defined")
            exit()
        return self.expand_node("__root__")
    
    def expand_node(self, node):
        capitalise = node[0].isupper()
        node = node.lower()
        option = random.choice(self.nodes[node])
        result = self.expand_option(option)
        if capitalise:
            result = result[0].upper() + result[1:]
        return result
    
    def expand_option(self, option):
        result = option;
        while result.find("{") != -1:
            start = result.find("{")
            end = result.find("}", start+1)
            if end == -1:
                die("on line %s the '{' at column %s has no matching '}': %s" % (self._lines.index(option)+1, start, option))
            node = result[start+1:end]
            if not node.lower() in self.nodes:
                die("on line %s the node {%s} does not exist or has no options: %s" % (self._lines.index(option)+1, node, option))
            result = result[:start] + self.expand_node(node) + result[end+1:]
        return result
    
    def validate(self):
        for node in self.nodes:
            for option in self.nodes[node]:
                self.expand_option(option)
        
    
    @staticmethod
    def from_file(path):
        grammar = Grammar()
        node = "__root__"
        for line in open(path):
            line = line.strip()
            grammar._lines.append(line)
            if len(line) == 0:
                continue # skip empty lines
            if line[0] == "#":
                continue # skip comments
            if line[0] == "[" and line[-1] == "]":
                node = line[1:-1]
            else:
                grammar.add_node_option(node.lower(), line)
        grammar.validate()
        return grammar


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print >> sys.stderr, "Usage: %s grammarfile" % sys.argv[0]
        exit(1)
    
    grammar = Grammar.from_file(sys.argv[1])
    print grammar.generate()
    