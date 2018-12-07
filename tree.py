class Tree:
    def __init__(self, data=None, parent=None):
        self.data = data
        self.parent = parent
        self.children = []

    def AddChild(self, data):
        self.children.append(Tree(data, self))

    def AddChildren(self, datas):
        for data in datas:
            self.AddChild(data)
