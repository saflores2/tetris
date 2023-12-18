import global_vars

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = global_vars.SHAPE_COLORS[global_vars.SHAPES.index(shape)]
        self.rotation = 0
