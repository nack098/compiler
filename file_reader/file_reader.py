from io import TextIOWrapper

class FileReader:
    file: TextIOWrapper = None

    def __iter__(self):
        return self

    def __next__(self):
        char = self.file.read(1)
        if not char:
            raise StopIteration
        return char

    def __call__(self, path:str):
        if self.file:
            self.file.close()
        self.file = open(path)
        return self
    
    def __del__(self):
        if self.file:
            self.file.close()
    
    def __len__(self):
        return len(self.file)