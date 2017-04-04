#!/usr/bin/env python3
import random

MASKS = {
    'square' : [
                [(0,0), (0,1), (1,0), (1,1)]
                ],
    'line'   : [
                [(0,0), (1,0), (2,0), (3,0)],
                [(0,0), (0,1), (0,2), (0,3)],
                ],
        }

class Piece(object):
    def __init__(self, which=None):
        global MASKS
        if which is None:
            which = random.choice([key for key in MASKS.keys()])
        self._mask_state = 0
        self._masks = MASKS[which]

    def mask(self, rot=0):
        return self._masks[self._mask_state_add(rot)]

    def _mask_state_add(self, num):
        while num < 0:
            num += len(self._masks)
        return (num + self._mask_state) % len(self._masks)

    def change_mask(self, num=1):
        self._mask_state = self._mask_state_add(num)

class TetrisModel(object):
    def __init__(self):
        self._width = 16
        self._height = 25
        self._grid = [' ' for i in range(0, self._width*self._height)]
        self._piece = None

    def tick(self):
        if not self.have_active_piece():
            self.spawn_new_piece()
        else:
            self.try_move_active_piece_down()

    def have_active_piece(self):
        return self._piece is not None

    def rotate(self, rot=1):
        if self.have_active_piece() and \
           self.render_active_piece(rot=1,
                                    row=self._piece_pos['row'],
                                    col=self._piece_pos['col']):
            self._piece.change_mask(num=rot)
            
    def slam(self):
        while self.have_active_piece():
            self.try_move_active_piece_down()

    def spawn_new_piece(self):
        self._piece = Piece()
        self._piece_pos = dict()
        self._piece_pos['row'] = 0
        self._piece_pos['col'] = self._width//2
        if not self.render_active_piece(rot=0, 
                                        row=self._piece_pos['row'],
                                        col=self._piece_pos['col']):
            self.game_over()

    def try_move_active_piece_down(self):
        if not self.render_active_piece(rot=0,
                                        row=self._piece_pos['row'] + 1,
                                        col=self._piece_pos['col']):
            self.anchor_active_piece()
            self.clear_contiguous_rows()
        else:
            self._piece_pos['row'] += 1

    def row_col_to_index(self, row=0, col=0):
        return row*self._width+col

    def anchor_active_piece(self):
        self._piece = None

    def clear_contiguous_rows(self):
        pass
    #todo

    def render_active_piece(self, rot=0, row=0, col=0):
        opnts = [[pnt[0] + self._piece_pos['col'],
                  pnt[1] + self._piece_pos['row']]
                  for pnt in self._piece.mask()]
        npnts = [[pnt[0] + col, pnt[1] + row] for pnt in self._piece.mask(rot=rot)]
        
        for pnt in opnts:
            self.clear_point(row=pnt[1], col=pnt[0])
        
        failed = False
        for pnt in npnts:
            if self.point_is_occupied(row=pnt[1], col=pnt[0]):
                failed = True

        pnts = opnts if failed else npnts

        for pnt in pnts:
            self.set_point(row=pnt[1], col=pnt[0])

        return not failed
        
    def set_point(self, row=0, col=0):
        self._grid[self.row_col_to_index(row=row, col=col)] = 'X'

    def clear_point(self, row=0, col=0):
        self._grid[self.row_col_to_index(row=row, col=col)] = ' '

    def point_is_occupied(self, row=0, col=0):
        return self._grid[self.row_col_to_index(row=row, col=col)] != ' '
        
    def render_to_stdout(self):
        for row in range(0, self._height):
            print("".join(self._grid[self._width*row:self._width*row+self._width]))

def main():
    print("tetris!")
    game = TetrisModel()
    game.tick()
    game.tick()
    game.rotate(1)
    game.render_to_stdout()


if __name__ == "__main__":
    main()
