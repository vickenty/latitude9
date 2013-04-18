"""
1. User should be allowed to play computer
2. Computer should know the following   
    1. where it needs to go to win
    2. how to pick up different weapons (rock paper scissors)
    3. what it needs to pick up in order to get to the end
"""

class ComputerPlayer:

    def __init__(self,player):
        self.player = player

    def next_move(self):
        next_move = self.prioritize_legal_moves
        if (next_move == 0):
            return self.player.move(0,1) 
        
        if (next_move == 1):
            return self.player.move(0,-1)

        if (next_move == 2):
            return self.player.move(-1,0);
            
        if (next_move == 3):
            return move_right(1)

        if (next_move == -1):
            skip_turn

    """ 
    This method prioritizes all legal moves based on 
    1. what the current objective is
        if objective is to get to finish line, then 
        player should get closer to the finish line
        if objective is duel the opponent, get closer to 
        opponent
        remember move_list is in the order up,down,left right
    """
    def priortize_legal_moves(self):
        move_list = self.legal_moves

        final_x,final_y = self.player.next_goal
        high_pri = -1
        min_distance  = 0
        if (move_list[0] == 1):
            if (min_distance > self.player.distance_between(final_x,final_y)):
                high_pri = 0        
            
        if (move_list[1] == 1):
            if (min_distance > self.player.distance_between(final_x,final_y)):
                high_pri = 1
        
        if (move_list[2] == 1):
            if (min_distance > self.player.distance_between(final_x,final_y,self.pos_x-1,self.pos_y)):
                high_pri = 2

        if (move_list[3] == 1):
            if (min_distance > self.player.distance_between(final_x,final_y,self.pos_x,self.pos_y-1)):
                high_pri = 3

        return high_pri
        
    """ 
    gets list of legal moves
    typically user can either move one pixel up,down right left
    This method will return an array with 4 elements
    the 4 elements correspond to up,down, right, left
    If the element is 1 then the move is legal
    else it is not
    """

    def legal_moves(self):
        move_array = [0,0,0,0]
        move_array[0] = self.player.walkable(pos_x,pos_y-1)
        move_array[1] = self.player.walkable(pos_x,pos_y+1)
        move_array[2] = self.player.walkable(pos_x-1,pos_y)
        move_array[3] = self.player.walkable(pos_x+1,pos_y)
        return move_array


    def can_move(self,x_pos,y_pos):
        """ When can a move not take place
            when the pixel is covered by a wall.
            when self.pos is more than 1 pixel away.
        """

        if ((self.pos_x - x_pos) > 1):
            return 0

        if ((self.pos_y - y_pos) > 1):
            return 0

        return (is_part_of_wall(x_pos,y_pos))  


    def go_there(self,nx,ny,visited_nodes):
        x = self.player.x
        y = self.player.y

        if (x,y) in visted_nodes:
            return visited_nodes


    def distance_between(start,end):
        if start == end:
            return 0
        else if 

    def dijkstra(self,nx,ny):
        start_cell = Cell(cur_x,cur_y)
        end_cell = Cell(nx,ny)
        visited_cells = {};
        distance = {}
        visited_cells[start_cell] = 1
        distance{start_cell} = 0
        previous = {}

        for cell in visited_cells:
            if cell == end:
                break
            neighbour_nodes = cell.neighbours(cur_x, cur_y)
            for neighbour_cell in neighbour_nodes:   
                cur_distance = distance[cell] + 1
                if distance.has_key(neighbour_cell):
                    if cur_distance < distance[neighbour_cell]:
                        distance[neighbour_cell] = cur_distance
                        previous[neighbour_cell] = cell
                elif !visited_cells.has_key(neighbor_cell):
                    visited_cells[neighbour_cell] = 1
                    distance[neighbour_cell] = cur_distance
                    previous[neighbour_cell] = cell


         return distance,previous 
                        
                        
                            
                    
                
            
           
        
        
        
