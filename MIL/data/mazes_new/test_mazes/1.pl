:-multifile(step_up/2).
:-multifile(step_down/2).
:-multifile(step_left/2).
:-multifile(step_right/2).
:-multifile(testing_instance/3).
testing_instance(solve,1,solve([1,10/6,s],[1,7/8,e])).
step_up([1,6/6,f],[1,6/7,f]).
step_down([1,6/7,f],[1,6/6,f]).
step_up([1,6/7,f],[1,6/8,f]).
step_right([1,6/8,f],[1,7/8,e]).
step_down([1,6/8,f],[1,6/7,f]).
step_up([1,6/8,f],[1,6/9,f]).
step_down([1,6/9,f],[1,6/8,f]).
step_up([1,6/9,f],[1,6/10,f]).
step_right([1,6/10,f],[1,7/10,f]).
step_down([1,6/10,f],[1,6/9,f]).
step_left([1,7/8,e],[1,6/8,f]).
step_right([1,7/8,e],[1,8/8,f]).
step_left([1,7/10,f],[1,6/10,f]).
step_right([1,7/10,f],[1,8/10,f]).
step_right([1,8/6,f],[1,9/6,f]).
step_left([1,8/8,f],[1,7/8,e]).
step_right([1,8/8,f],[1,9/8,f]).
step_left([1,8/10,f],[1,7/10,f]).
step_right([1,8/10,f],[1,9/10,f]).
step_left([1,9/6,f],[1,8/6,f]).
step_right([1,9/6,f],[1,10/6,s]).
step_left([1,9/8,f],[1,8/8,f]).
step_right([1,9/8,f],[1,10/8,f]).
step_left([1,9/10,f],[1,8/10,f]).
step_right([1,9/10,f],[1,10/10,f]).
step_left([1,10/6,s],[1,9/6,f]).
step_up([1,10/6,s],[1,10/7,f]).
step_down([1,10/7,f],[1,10/6,s]).
step_up([1,10/7,f],[1,10/8,f]).
step_left([1,10/8,f],[1,9/8,f]).
step_down([1,10/8,f],[1,10/7,f]).
step_left([1,10/10,f],[1,9/10,f]).
