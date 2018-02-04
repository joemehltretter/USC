####################################################################
#                                                                  #
# CreateMove.py takes a move as the input and creates a new        #
# move instance where the move information is stored and can be    #
# referenced.                                                      #
#                                                                  # 
####################################################################
import BoardConfig

class CreateMove(object):
  def __init__(self, row, column, position, player):
    self.row = row
    self.column = column
    self.position = position
    self.player = player
    

    
