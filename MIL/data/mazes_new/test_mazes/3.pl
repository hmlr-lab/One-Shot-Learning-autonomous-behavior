:-multifile(step_up/2).
:-multifile(step_down/2).
:-multifile(step_left/2).
:-multifile(step_right/2).
:-multifile(testing_instance/3).
testing_instance(solve,3,solve([3,10/6,s],[3,10/10,e])).
step_right([3,6/6,f],[3,7/6,f]).
step_up([3,6/6,f],[3,6/7,f]).
step_down([3,6/7,f],[3,6/6,f]).
step_up([3,6/7,f],[3,6/8,f]).
step_down([3,6/8,f],[3,6/7,f]).
step_up([3,6/8,f],[3,6/9,f]).
step_down([3,6/9,f],[3,6/8,f]).
step_up([3,6/9,f],[3,6/10,f]).
step_right([3,6/10,f],[3,7/10,f]).
step_down([3,6/10,f],[3,6/9,f]).
step_left([3,7/6,f],[3,6/6,f]).
step_right([3,7/6,f],[3,8/6,f]).
step_left([3,7/10,f],[3,6/10,f]).
step_right([3,7/10,f],[3,8/10,f]).
step_left([3,8/6,f],[3,7/6,f]).
step_right([3,8/6,f],[3,9/6,f]).
step_up([3,8/6,f],[3,8/7,f]).
step_down([3,8/7,f],[3,8/6,f]).
step_up([3,8/7,f],[3,8/8,f]).
step_down([3,8/8,f],[3,8/7,f]).
step_left([3,8/10,f],[3,7/10,f]).
step_right([3,8/10,f],[3,9/10,f]).
step_left([3,9/6,f],[3,8/6,f]).
step_right([3,9/6,f],[3,10/6,s]).
step_left([3,9/10,f],[3,8/10,f]).
step_right([3,9/10,f],[3,10/10,e]).
step_left([3,10/6,s],[3,9/6,f]).
step_up([3,10/8,f],[3,10/9,f]).
step_down([3,10/9,f],[3,10/8,f]).
step_up([3,10/9,f],[3,10/10,e]).
step_left([3,10/10,e],[3,9/10,f]).
step_down([3,10/10,e],[3,10/9,f]).
