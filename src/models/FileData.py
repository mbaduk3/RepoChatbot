class FileData:

    def __init__(self, path, filename, module, content, functions, classes):
        self.path = path
        self.filename = filename
        self.module = module
        self.content = content
        self.lines = content.count("\n") + 1
        self.functions = functions
        self.classes = classes