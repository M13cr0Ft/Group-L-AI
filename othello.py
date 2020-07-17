import copy
import time
import random
EMPTY = 'e';
BLACK = 'b';
WHITE = 'w';
INVALID = 'X';
UP = -10;
DOWN = 10;
RIGHT = 1;
LEFT = -1;
UP_RIGHT = -9;
UP_LEFT = -11;
DOWN_RIGHT = 11;
DOWN_LEFT = 9;
seen = set();
DIRECTIONS = (UP, DOWN, LEFT, RIGHT, UP_RIGHT, UP_LEFT, DOWN_RIGHT, DOWN_LEFT);
def reverse(color):
  return (WHITE if color==BLACK else BLACK);
class othello():
  def __init__(self):
    self.board = [];
    self.color = BLACK;
    for i in range(100):
      if i<10 or i%10==0 or i>89 or i%10==9:
        self.board.append(INVALID);
      elif i==44 or i==55:
        self.board.append(WHITE);
      elif i==45 or i==54:
        self.board.append(BLACK);
      else:
        self.board.append(EMPTY);
  def dump(self):
    str = "";
    for i in range(100):
      if i%10==0:
        print(str);
        str = "";
      str += self.board[i];
      str += " ";
    print(str);
    print(("black" if self.color==BLACK else "white") + "\'s turn to play");
        
  def as_2d(self):
    new_arr = [];
    for i in range(10):
      tmp_arr = [];
      for j in range(10):
        tmp_arr.append(self.board[j*10+i]);
      new_arr.append(tmp_arr);
    return new_arr;
  def as_1d(self):
    return self.arr;
  def as_tuple(self):
    return tuple(map(tuple, self.as_2d())); 
  def __eq__(self, other_val):
    for i in range(100):
      if not self.board[i]==other_val.board[i]:
        return False;
    return True;
  def testMove(self, loc):
    if not self.board[loc]==EMPTY:
      return False;
    for i in DIRECTIONS:
      location = loc + i;
      cond = False;
      while self.board[location]==reverse(self.color):
        location += i;
        cond = True;
      if cond==False:
        continue;
      if self.board[location]==self.color:
        return True;
    return False;
  def playMove(self, loc):
    self.board[loc] = self.color;
    self.move = loc;
    for i in DIRECTIONS:
      location = loc + i;
      while self.board[location]==reverse(self.color):
        location += i;
      if self.board[location]==self.color:
        counter = loc + i;
        if i > 0:
          while counter < location:
            self.board[counter] = self.color;
            counter += i;
        else:
          while counter > location:
            self.board[counter] = self.color;
            counter += i;
    self.color = reverse(self.color);
    return self;
  def can_play(self):
    for i in range(100):
      if self.testMove(i):
        return True;
    return False;  
  def children(self):
    children = [];
    for i in range(100):
      if self.testMove(i):
        tmp = copy.deepcopy(self);
        tmp.playMove(i);
        children.append(tmp);
    return children;
  def evaluate(self, heuristics_map, color):
    value = 0;
    for i in range(100):
      if self.board[i]==WHITE:
        value -= heuristics_map[i];
      if self.board[i]==BLACK:
        value += heuristics_map[i];
    return value;


    
  def minimax(self, depth, color, alpha_beta, heuristics_map = [1] * 100):
    global seen;
    if tuple(self.board) in seen:
      return alpha_beta;
    else:
      seen.add(tuple(self.board));
    if not self.can_play():
      return (float('inf') if self.winner() else float('-inf'));
    if depth==0:
      if color==self.color:
        best_val = float("-inf");
        for i in range(100):
          if self.testMove(i):
            tmp = copy.deepcopy(self);
            best_val = max(best_val, tmp.playMove(i).evaluate(heuristics_map, color));
            if best_val > alpha_beta:
              return best_val;
        return best_val;
      else:
        worst_val = float("inf");
        for i in range(100):
          if self.testMove(i):
            tmp = copy.deepcopy(self);
            worst_val = min(worst_val, tmp.playMove(i).evaluate(heuristics_map, color));
            if worst_val < alpha_beta:
              return worst_val;
        return worst_val;
    else:
      if color==self.color:
        best_val = float('-inf');
        tmp = self.children();
        tmp.sort(key=lambda x: x.evaluate(heuristics_map, color), reverse=True);
        for i in tmp:
          best_val = max(best_val, i.minimax(depth-1, color, best_val, heuristics_map));
          if best_val > alpha_beta:
            return best_val;
        return best_val;
      else:
        worst_val = float("inf");
        tmp = self.children();
        tmp.sort(key=lambda x: x.evaluate(heuristics_map, color), reverse=False);
        for i in tmp:
          worst_val = min(worst_val, i.minimax(depth-1, color, worst_val, heuristics_map));
          if worst_val < alpha_beta:
            return worst_val;
        return worst_val;


  def find_best_move(self,depth, heuristics_map = [1] * 100):
    global seen;
    seen = set();
    best_value = float('-inf');
    best_move = -1;
    valid_move=False;
    for i in range(100):
      if self.testMove(i):
        valid_move=True;
        tmp = copy.deepcopy(self);
        tmp.playMove(i);
        value = tmp.minimax(depth, self.color, best_move, heuristics_map);
        if value > best_value:
          best_value = value;
          best_move = tmp.move;
    return best_move;

    
  def winner(self):
    value = 0;
    for i in range(100):
      if self.board[i]==WHITE:
        value-=1;
      if self.board[i]==BLACK:
        value+=1;
    return 1 if value < 0 else 0;
  def win_by(self):
    value = 0;
    for i in range(100):
      if self.board[i]==WHITE:
        value-=1;
      if self.board[i]==BLACK:
        value+=1;
    return value;
def compare(hmap1, hmap2, depth_allowed, dump=False):
  new_game = othello();
  turn = False;
  while new_game.can_play():
    move = new_game.find_best_move(depth_allowed, hmap1 if turn==False else hmap2);
    if dump:
      print(("black" if new_game.color==BLACK else "white"), "is playing the move ", move);
    new_game.playMove(move);
    turn = not turn;
  return new_game.winner();
game = othello();
time_now = time.time();
game.find_best_move(4);
print((time.time()-time_now)*1000);


#mygame = othello();

#mygame.dump();
test = [];
#print(("black" if mygame.color==BLACK else "white"), "\'s best move is:", mygame.find_best_move(5, [1] * 100));

#fight against randy:
good_map = [0,0,0,0,0,0,0,0,0,0,0,8,1,2,2,2,2,1,8,0,0,1,2,2,2,2,2,2,1,0,0,2,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,0,0,1,2,2,2,2,2,2,1,0,0,8,1,2,2,2,2,1,8,0,0,0,0,0,0,0,0,0,0,0];
normal_map = [1] * 100;
#print(("good_map" if compare(good_map, normal_map, 2) else "normal_map"), "won!");
#print(("normal_map" if compare(normal_map, good_map, 2) else "good_map"), "won!");
random.seed();
def test_ai(debug = False):
  game = othello();
  turn = False;
  while game.can_play():
    if turn:
      children = game.children();
      game.playMove(children[random.randint(0, len(children)-1)]);
    else:
      game.playMove(game.find_best_move(2));
    if debug:
      print(("black" if game.color==WHITE else "white"), "played the move", game.move);
  return game.win_by();
random.seed();
print("minimax beat randy by ", test_ai(), " points!!!");
print("minimax beat randy by ", test_ai(), " points!!!");
print("minimax beat randy by ", test_ai(), " points!!!");