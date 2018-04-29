
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'left+-left*/leftPOWERrightUMINUSCOS DERIVATIVE FLOAT FROM GOES INFINITY INT INTEGRAL LIMIT OF POWER PRINTLIST PRODUCT SIN SUM TAN TO VAR WHEN Xstatement : VAR "=" expressionstatement : expressionexpression : expression \'+\' expression\n                  | expression \'-\' expression\n                  | expression \'*\' expression\n                  | expression \'/\' expression\n                  | expression POWER expressionexpression : \'-\' expression %prec UMINUSexpression : \'(\' expression \')\'expression : INTexpression : VARexpression : Xexpression : SIN \'(\' expression \')\'\n                | COS \'(\' expression \')\'\n                | TAN \'(\' expression \')\' expression : SUM FROM expression TO expression OF expression'
    
_lr_action_items = {'INT':([0,2,5,14,16,17,18,19,20,21,22,23,24,38,41,],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,]),'OF':([1,3,13,15,25,30,31,32,33,34,36,37,39,40,42,],[-10,-12,-11,-8,-9,-5,-4,-6,-3,-7,-15,-13,-14,41,-16,]),'(':([0,2,4,5,6,11,14,16,17,18,19,20,21,22,23,24,38,41,],[2,2,14,2,16,24,2,2,2,2,2,2,2,2,2,2,2,2,]),'FROM':([7,],[17,]),'=':([8,],[18,]),'VAR':([0,2,5,14,16,17,18,19,20,21,22,23,24,38,41,],[8,13,13,13,13,13,13,13,13,13,13,13,13,13,13,]),'POWER':([1,3,8,9,12,13,15,25,26,27,28,29,30,31,32,33,34,35,36,37,39,40,42,],[-10,-12,-11,23,23,-11,-8,-9,23,23,23,23,23,23,23,23,-7,23,-15,-13,-14,23,23,]),'/':([1,3,8,9,12,13,15,25,26,27,28,29,30,31,32,33,34,35,36,37,39,40,42,],[-10,-12,-11,21,21,-11,-8,-9,21,21,21,21,-5,21,-6,21,-7,21,-15,-13,-14,21,21,]),')':([1,3,12,13,15,25,26,27,30,31,32,33,34,35,36,37,39,42,],[-10,-12,25,-11,-8,-9,36,37,-5,-4,-6,-3,-7,39,-15,-13,-14,-16,]),'SUM':([0,2,5,14,16,17,18,19,20,21,22,23,24,38,41,],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,]),'X':([0,2,5,14,16,17,18,19,20,21,22,23,24,38,41,],[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,]),'TAN':([0,2,5,14,16,17,18,19,20,21,22,23,24,38,41,],[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,]),'*':([1,3,8,9,12,13,15,25,26,27,28,29,30,31,32,33,34,35,36,37,39,40,42,],[-10,-12,-11,19,19,-11,-8,-9,19,19,19,19,-5,19,-6,19,-7,19,-15,-13,-14,19,19,]),'-':([0,1,2,3,5,8,9,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,],[5,-10,5,-12,5,-11,20,20,-11,5,-8,5,5,5,5,5,5,5,5,5,-9,20,20,20,20,-5,-4,-6,-3,-7,20,-15,-13,5,-14,20,5,20,]),'SIN':([0,2,5,14,16,17,18,19,20,21,22,23,24,38,41,],[6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,]),'TO':([1,3,13,15,25,28,30,31,32,33,34,36,37,39,42,],[-10,-12,-11,-8,-9,38,-5,-4,-6,-3,-7,-15,-13,-14,-16,]),'COS':([0,2,5,14,16,17,18,19,20,21,22,23,24,38,41,],[11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,]),'+':([1,3,8,9,12,13,15,25,26,27,28,29,30,31,32,33,34,35,36,37,39,40,42,],[-10,-12,-11,22,22,-11,-8,-9,22,22,22,22,-5,-4,-6,-3,-7,22,-15,-13,-14,22,22,]),'$end':([1,3,8,9,10,13,15,25,29,30,31,32,33,34,36,37,39,42,],[-10,-12,-11,-2,0,-11,-8,-9,-1,-5,-4,-6,-3,-7,-15,-13,-14,-16,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,2,5,14,16,17,18,19,20,21,22,23,24,38,41,],[9,12,15,26,27,28,29,30,31,32,33,34,35,40,42,]),'statement':([0,],[10,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> VAR = expression','statement',3,'p_statement_assign','calc.py',109),
  ('statement -> expression','statement',1,'p_statement_expr','calc.py',114),
  ('expression -> expression + expression','expression',3,'p_expression_binop','calc.py',119),
  ('expression -> expression - expression','expression',3,'p_expression_binop','calc.py',120),
  ('expression -> expression * expression','expression',3,'p_expression_binop','calc.py',121),
  ('expression -> expression / expression','expression',3,'p_expression_binop','calc.py',122),
  ('expression -> expression POWER expression','expression',3,'p_expression_binop','calc.py',123),
  ('expression -> - expression','expression',2,'p_expression_uminus','calc.py',138),
  ('expression -> ( expression )','expression',3,'p_expression_group','calc.py',143),
  ('expression -> INT','expression',1,'p_expression_number','calc.py',148),
  ('expression -> VAR','expression',1,'p_expression_name','calc.py',153),
  ('expression -> X','expression',1,'p_equation_x','calc.py',162),
  ('expression -> SIN ( expression )','expression',4,'p_expression_trigonometry','calc.py',167),
  ('expression -> COS ( expression )','expression',4,'p_expression_trigonometry','calc.py',168),
  ('expression -> TAN ( expression )','expression',4,'p_expression_trigonometry','calc.py',169),
  ('expression -> SUM FROM expression TO expression OF expression','expression',7,'p_expression_sum','calc.py',174),
]
