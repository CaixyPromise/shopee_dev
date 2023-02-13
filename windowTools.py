from tkinter.ttk import Treeview


class TreeViewUtils(Treeview):
    def __init__(self, parent, **args):
        Treeview.__init__(self, parent,  **args)
        self.pack(fill = 'both', expand = True)

        for i, column in enumerate(self['columns']):
            self.column(column, width = 100, anchor = args.get('anchor', 'center'))
            self.heading(column, text = column,
                              command = lambda _col = column: self.sort_tree(self, _col, False)
                              )

    def insert_data(self, values, parent = '', index = 'end', item = None):
        self.insert(parent, index, item, values = values)

    def sort_tree(self, tree, col, reverse):
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        l.sort(key = lambda t: t[0], reverse = reverse)

        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)
        tree.heading(col, command = lambda _col = col: self.sort_tree(tree, _col, not reverse))

    def delete_item(self, item):
        self.delete(item)

    def update_item(self, item, values):
        for i, value in enumerate(values):
            self.item(item, values = (value,))

    def search_item(self, values):
        for item in self.get_children():
            if self.item(item)["values"] == values:
                return item
        return None

    def bindEvent(self, event_name, func):
        self.bind(event_name, func)

