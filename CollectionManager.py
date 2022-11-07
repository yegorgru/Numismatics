from CollectionPreviewFrameRow import CollectionPreviewFrameRow, CollectionPreviewFrame


class CollectionManager:
    def __init__(self, controller):
        self.controller = controller

    def pack_collections(self, parent, collections_rs, width):
        CollectionPreviewFrameRow(parent, self.controller, [(CollectionPreviewFrame.PLUS_COLLECTION, None)]).pack()
        while True:
            result = collections_rs.fetchmany(width)
            if not result:
                break
            else:
                CollectionPreviewFrameRow(parent, self.controller, result).pack()