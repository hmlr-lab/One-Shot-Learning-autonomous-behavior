:-module(move_generator, [write_primitives/0
                         ,write_moves/1
                         ,generate_moves/2
                         ,passable_tiles/3
                         ,passable_tile/3
                         ,map_location/5
                         ,start_location/3
                         ,end_location/3
                         ]).

:-use_module(generator_configuration).

/** <module> Generate primitive moves for maze solvers.

This module exports predicates used to generate primitive moves over a
grid-world style map, currently representing the map of a maze. The set
of primitive moves generated for each map is the set of all permitted
moves in the map, i.e. moves that don't try to step into walls.


__ Write primitives file __

The primitive moves for each map are written to a Prolog module file by
write_moves/1.

Example of calling write_moves/1:

==
?- move_generator:write_moves(data(drafts/ijcai_2024/mazes/'primitives.pl')).
==


__ Map format __

Maps should be in the form of atoms maze(Id,Dims,Rows) where Id is a
constant used as an identifier for the map, Dims is a pair Max_x-Max_y,
listing the dimensions of the map, and Rows is a list-of-lists, where
each sub-list is a row in the map, and each element in a sub-list is a
"tile" on the map.

Example of a maze/3 atom:
==
maze(short_2, 3-3, [[s, f, w], [w, f, w], [w, e, w]]).
==

In the above example, short_2 is the identifier of the maze, 3-3 are the
dimensions of the maze map and [[s, f, w], [w, f, w], [w, e, w]] are the
rows in the map.

The elements in each row are constants that represent the type of
terrain on that tile. Mazes have three types of terrain: s[tart], for
the entry point of the maze, e[nd], for the exit from the maze, w[all]
and f[loor] for unpassable wall, and passable floor tiles, respectively.

See map_display.pl for predicates to pretty-print a map at the Prolog
console.


__ Move generation __

Moves are generated with a call to generate_moves/2. The first argument
is the identifier of the maze for which moves are to be printed.

Example of use of generate_moves/2; maze map included for reference.

==
% Maze locations and tiles
%
% 0/2.s 1/2.f 2/2.w
% 0/1.w 1/1.f 2/1.w
% 0/0.w 1/0.e 2/0.w

?- generate_moves(short_2,_Vs), maplist(portray_clause,_Vs).
step_down([short_2, 1/1, f, Vs], [short_2, 1/0, e, [d|Vs]]).
step_down([short_2, 1/2, f, Vs], [short_2, 1/1, f, [d|Vs]]).
step_left([short_2, 1/2, f, Vs], [short_2, 0/2, s, [l|Vs]]).
step_right([short_2, 0/2, s, Vs], [short_2, 1/2, f, [r|Vs]]).
step_up([short_2, 1/0, e, Vs], [short_2, 1/1, f, [u|Vs]]).
step_up([short_2, 1/1, f, Vs], [short_2, 1/2, f, [u|Vs]]).
true.
==

Each generated move must both begin and end in a passable tile. Passable
tiles are defined by the predicate passable/1:

==
passable(f).
passable(s).
passable(e).
==

That means that, in maze maps, only floor, start and end tiles are
passable. That in turn means that only moves from and to start, end and
floor tiles will be generated by generate_moves/2, so there's no
possibility of moving through a wall.

Generated moves currently do not include a "stay" move that begins and
ends in the same coordinates.


__ Map topology __

In map/3 atoms maps are given as lists in what is essentially row-major
order (i.e. each sub-list is a row).

The natural way to index through a map in that row-major list form in
Prolog is with two consecutive calls to nth0/3 (or nth1/3 for a 1-based
index).

The first call to nth0/3 walks over the sub-lists representing rows and
its first argument is bound to the index of a row, i.e. the y dimension
of the map.

==
?- move_generator:maze(short_1,_Dims,_Ms), nth0(I,_Ms,Row).
I = 0,
Row = [s, w] ;
I = 1,
Row = [e, w].
==

The second call to nth0/3 walks over the elements of sub-lists
representing tiles and its first argument is bound to the index of a
column, i.e. the x dimension of the map.

==
?- move_generator:maze(short_1,_Dims,_Ms), nth0(I,_Ms,Row), nth0(K,Row,Tile).
I = K, K = 0,
Row = [s, w],
Tile = s ;
I = 0,
Row = [s, w],
K = 1,
Tile = w ;
I = 1,
Row = [e, w],
K = 0,
Tile = e ;
I = K, K = 1,
Row = [e, w],
Tile = w.
==

This natural way effectively places the origin of the map, i.e. its 0/0
x/y coordinates, at the top-left of the map. We want instead to treat a
map as a Cartesian plane, with the origin at the _bottom_ left (because
that makes it easier to apply concepts like Euclidean distance, for
example).

For this reason, predicates that generate or test map locations can
apply a rotation to a pair of coordinates to transform them into
Cartesian coordinates. Below are some examples.

map_location/5 generates locations in a map. The last argument is a
Boolean ('true' or 'false') that determines whether the map coordinates
are rotated ('true') or not ('false'):

==
?- _Rot = false, move_generator:maze(short_1,_Dims,_Ms), map_location(Xt/Yt,T,_Ms,_Dims,_Rot).
Xt = Yt, Yt = 0,
T = s .

?- _Rot = true, move_generator:maze(short_1,_Dims,_Ms), map_location(Xt/Yt,T,_Ms,_Dims,_Rot).
Xt = 0,
Yt = 1,
T = s .
==

In the example above, note that with the rotation argument given as
'false', the entry tile of the maze ('s') in the short_1 map is at x/y =
0/0, whereas with the rotation argument 'true' the entry tile is at x/y
= 0/1.

passable_tile/3 and passable_tiles/3 can generate all passable tiles, or
check whether tiles are passable. Both predicates apply a rotation by
default.

==
?- move_generator:maze(short_1,_Dims,_Ms), passable_tiles(_Ms,_Dims,_Ts), maplist(writeln,_Ts).
0/1
0/0
true.

?- move_generator:maze(short_1,_Dims,_Ms), passable_tile(X/Y,_Ms,_Dims).
X = 0,
Y = 1 ;
X = Y, Y = 0 ;
false.
==

The x and y coordinates of the start and end locations of a maze can be
obtained with start_location/2 and end_location/2. Both predicates apply
a rotation by default.

==
?- move_generator:maze(short_1,_Dims,_Ms), start_location(_Ms,_Dims,X/Y).
X = 0,
Y = 1 ;
false.

?- move_generator:maze(short_1,_Dims,_Ms), end_location(_Ms,_Dims,X/Y).
X = Y, Y = 0 ;
false.
==

Note that generated moves apply a rotation to the map coordinates.


__ Other maps __

The representation of maps in this file can be extended with more types
of tiles, or with tiles represented as compound terms. This can be used
to model other kinds of problem than maze solving.

As a for instance, the Wumpus World problem can be modelled with tiles
of the form t(W,S,P,G), where each of W, S, P, G are booleans (either
't' for true or 'f' for false) denoting the presence of a W[umpus],
S[tench], P[it] or bar of G[old], respectively.


*/

%!      load_mazes is det.
%
%       Load generated files from a traditional Prolog file.
%
%       This predicate loads maze maps generated by James' map generator
%       so that they can be used to generate primitive moves, to use as
%       background knowledge. The same maps are then saved into a new,
%       module, file along with their primitive moves.
%
%       The path to the maze file is defined in maze_file/1 and the path
%       to the primitives file, and its module name, in
%       primitives_file/2, both found in generator_configuration.pl.
%
load_mazes:-
        forall(generator_configuration:maze_file(P)
              ,ensure_loaded(P)).

:-load_mazes.


%!      passable(?Symbol) is semidet.
%
%       Symbol of a passable tile in a map.
%
%       Passable tiles can be traversed by an agent. Other tiles,
%       cannot.
%
passable(f).
passable(s).
passable(e).



%!      write_primitives is det.
%
%       Write primitive moves to a file.
%
%       The path of the primitives file is determined by the
%       configuration option primitives_file in
%       generator_configuration.pl.
%
write_primitives:-
        generator_configuration:primitives_file(P,_)
        ,load_mazes
        ,write_moves(P).



%!      write_moves(+File) is det.
%
%       Write primitive moves to the given File.
%
%       Filename must be an atom or compound term expandable to a file
%       path.
%
%       write_moves/1 will write to that file a Prolog module with the
%       primitive moves (step_up/2, step_down/2, step_left/2,
%       step_right/2) generatred by generate_moves/2.
%
%       The generated file can then be imported into an experiment file
%       in Louise to run maze solving experiments.
%
write_moves(F):-
        definition_module(D)
        ,S = (expand_file_search_path(F,F_)
            ,open(F_,write,Stm,[alias(primitives_file)
                      ,close_on_abort(true)
                      ])
            )
        ,G = (H = (:-module(primitives,[maze/3
                                       ,step_down/2
                                       ,step_left/2
                                       ,step_right/2
                                       ,step_up/2
                                       ])
                  )
             ,portray_clause(Stm,H)
             ,nl(Stm)
             ,Ds = [:-discontiguous(maze/3)
                   ,:-discontiguous(step_down/2)
                   ,:-discontiguous(step_up/2)
                   ,:-discontiguous(step_left/2)
                   ,:-discontiguous(step_right/2)
                   ]
             ,maplist(portray_clause(Stm),Ds)
             ,nl(Stm)
             ,portray_clause(Stm,:-multifile maze/3)
             ,nl(Stm)
             ,forall(D:maze(Id,Dims,Ms)
                     ,(generate_moves(Id,Vs)
                      ,format(Stm,'%Maze ~w~n',[Id])
                      ,portray_clause(Stm,maze(Id,Dims,Ms),[indent(1)])
                      ,nl(Stm)
                      ,format(Stm,'%Primitive moves for maze ~w~n',[Id])
                      ,maplist(portray_clause(Stm),Vs)
                      ,nl(Stm)
                      )
                    )
             ,abolish(move_generator:maze/3)
             )
        ,C = close(Stm)
        ,setup_call_cleanup(S,G,C).



%!      generate_moves(+Id,-Moves) is det.
%
%       Generate all possible Moves in a maze.
%
%       Id is the Id of a maze/2 term, storing the map of the maze as a
%       list-of-lists, where each sub-list is a row of the map. See the
%       module comments at the start of this file for more details on
%       map topology.
%
%       Moves is a list of atoms of the predicates step_up/2,
%       step_down/2, step_right/2, step_left/2, as generated by the
%       eponymous predicates in this module.
%
generate_moves(Id,Vs):-
        generator_configuration:action_representation(R)
        ,definition_module(D)
        ,D:maze(Id,Dims,Ms)
        ,passable_tiles(Ms,Dims,Ts)
        ,findall(M
                ,(member(X/Y,Ts)
                 ,move(R,maze(Id,Dims,Ms),X/Y,M)
                 )
                ,Vs_)
        ,sort(Vs_,Vs).


%!      definition_module(-Module) is det.
%
%       Get the name of the definition Module of maze/3.
%
%       Needed because maze/3 may be loaded from a non-module Prolog
%       file into move_generator.pl, in which case its definition module
%       is 'move_generator', or from a primitives file in which case the
%       definition module is 'primitives', and the simplest way to know
%       for sure is to ask Prolog.
%
definition_module(move_generator):-
        current_predicate(move_generator:maze/3)
        ,!.
definition_module(primitives):-
        generator_configuration:primitives_file(_P,M)
        ,current_predicate(M:maze/3).


%!      move(+Representation,+Maze,+Coordinates,-Move) is det.
%
%       Generate a single Move to the given Coordinates.
%
%       Representation is the current value of game_configuration option
%       action_representation/1: one of [memoryless,stack_based].
%
%       Maze is a maze/3 term for the current maze map.
%
%       Move is an atom of one of step_up/2, step_down/2, step_right/2,
%       step_left/2, as generated by the eponymous predicates in this
%       module.
%
move(R,maze(Id,Dims,Ms),X/Y,M):-
        step_up(R,[maze(Id,Dims,Ms),X/Y],M).
move(R,maze(Id,Dims,Ms),X/Y,M):-
        step_down(R,[maze(Id,Dims,Ms),X/Y],M).
move(R,maze(Id,Dims,Ms),X/Y,M):-
        step_right(R,[maze(Id,Dims,Ms),X/Y],M).
move(R,maze(Id,Dims,Ms),X/Y,M):-
        step_left(R,[maze(Id,Dims,Ms),X/Y],M).


%!      step_up(+Representation,+Start,-Step) is det.
%
%       Generate a Step up from a Start location.
%
%       Representation is the current value of game_configuration option
%       action_representation/1: one of [memoryless,stack_based].
%
%       Start is a list [Maze,Coordinates] where Maze is an atom
%       maze(Id,Dims,Map), representing a maze map with its
%       identifier, dimensions, and list of tiles, and Coordinates is a
%       pair X/Y, the coordinates of the start location of the move to
%       be generated. See the start of the file for more on maze/3
%       terms.
%
%       Move is an atom of the step_up/2 primitive move. Each argument
%       of step_up/2 is a list of the form: [Id,X/Y,T,Vs], representing
%       the world-state at the start and end of the move, where:
%       * Id is the map identifier, for easy reference.
%       * X/Y are the coordinates at the start or end of the move.
%       * T are the coordinates of the tile at the X/Y coordinates.
%       * Vs is a list of constants naming moves: [u,d,l,r], for up,
%       down, left, right, moves, respectively. This predicate adds a
%       constant 'u' to the list of moves.
%
%       step_up/2 generates steps with a rotation applied to coordinates
%       to transform them into Cartesian coordinates, with the origin
%       at the lower-left corner.
%
step_up(stack_based,[maze(Id,Dims,Ms),X/Y],step_up([Id,X/Y,T,Vs],[Id,X_/Y_,T_,[u|Vs]])):-
        step(X/Y,+,0/1,Ms,Dims,X_/Y_)
        ,map_location(X/Y,T,Ms,Dims,true)
        ,map_location(X_/Y_,T_,Ms,Dims,true)
        ,Vs = '$VAR'('Vs').
step_up(memoryless,[maze(Id,Dims,Ms),X/Y],step_up([Id,X/Y,T],[Id,X_/Y_,T_])):-
        step(X/Y,+,0/1,Ms,Dims,X_/Y_)
        ,map_location(X/Y,T,Ms,Dims,true)
        ,map_location(X_/Y_,T_,Ms,Dims,true).


%!      step_down(+Representation,+Start,-Step) is det.
%
%       Generate a Step down from a Start location.
%
%       As step_up/2 but moves down.
%
step_down(stack_based,[maze(Id,Dims,Ms),X/Y]
         ,step_down([Id,X/Y,T,Vs],[Id,X_/Y_,T_,[d|Vs]])):-
        step(X/Y,-,0/1,Ms,Dims,X_/Y_)
        ,map_location(X/Y,T,Ms,Dims,true)
        ,map_location(X_/Y_,T_,Ms,Dims,true)
        ,Vs = '$VAR'('Vs').
step_down(memoryless,[maze(Id,Dims,Ms),X/Y],step_down([Id,X/Y,T],[Id,X_/Y_,T_])):-
        step(X/Y,-,0/1,Ms,Dims,X_/Y_)
        ,map_location(X/Y,T,Ms,Dims,true)
        ,map_location(X_/Y_,T_,Ms,Dims,true).


%!      step_left(+Representation,+Start,-Step) is det.
%
%       Generate a Step to the left of a Start location.
%
%       As step_up/2 but moves left.
%
step_left(stack_based,[maze(Id,Dims,Ms),X/Y]
         ,step_left([Id,X/Y,T,Vs],[Id,X_/Y_,T_,[l|Vs]])):-
        step(X/Y,-,1/0,Ms,Dims,X_/Y_)
        ,map_location(X/Y,T,Ms,Dims,true)
        ,map_location(X_/Y_,T_,Ms,Dims,true)
        ,Vs = '$VAR'('Vs').
step_left(memoryless,[maze(Id,Dims,Ms),X/Y],step_left([Id,X/Y,T],[Id,X_/Y_,T_])):-
        step(X/Y,-,1/0,Ms,Dims,X_/Y_)
        ,map_location(X/Y,T,Ms,Dims,true)
        ,map_location(X_/Y_,T_,Ms,Dims,true).


%!      step_right(+Representation,+Start,-Step) is det.
%
%       Generate a Step tot he right of a Start location.
%
%       As step_up/2 but moves right.
%
step_right(stack_based,[maze(Id,Dims,Ms),X/Y]
          ,step_right([Id,X/Y,T,Vs],[Id,X_/Y_,T_,[r|Vs]])):-
        step(X/Y,+,1/0,Ms,Dims,X_/Y_)
        ,map_location(X/Y,T,Ms,Dims,true)
        ,map_location(X_/Y_,T_,Ms,Dims,true)
        ,Vs = '$VAR'('Vs').
step_right(memoryless,[maze(Id,Dims,Ms),X/Y],step_right([Id,X/Y,T],[Id,X_/Y_,T_])):-
        step(X/Y,+,1/0,Ms,Dims,X_/Y_)
        ,map_location(X/Y,T,Ms,Dims,true)
        ,map_location(X_/Y_,T_,Ms,Dims,true).


%!      step(+Coords,+Delta,+Distance,+Map,+Dims,-Target) is
%!      det.
%
%       Take a step from an initial pair of coordinates.
%
%       Coords is a pair X/Y, where X,Y are integers representing a pair
%       of coordinates in the 2-dimensional Cartesian plane with its
%       origin at (0,0). Think of X as the "columns", the Y as the
%       "rows", starting the count at the bottom-left of a 2D grid.
%
%       Delta is one of [+,-], denoting how the given pair of
%       Coordinates is to be modified by the primitive move. "-"
%       increments and "+" decrements, each of X and Y, according to
%       Distance.
%
%       Distance is a pair Dx/Dy, where Dx, Dy are integers,
%       representing the amount by which the corresponding coordinate, X
%       for Dx, Y for Dy, in Coordinates is to be modified by this move.
%
%       Map is a list-of-lists representing a map of a 2-dimensional
%       grid world (imagine this world overlayed onto the Cartesian
%       plane; or the other way around). Each sub-list is a row in the
%       grid. Each element of a sub-list, i.e. the content of a "cell"
%       in the grid, is a constant representing the type of terrain of
%       that map tile. A move can only begin and end in a "passable" map
%       tile. More categories of tiles may be added later. See comments
%       ar the start of the file for more on map topology.
%
%       Dims is a pair Max_x - Max_y listing the limits of the two map
%       dimensions.
%
%       This predicate applies a Cartesian rotation to map coordinates.
%
step(X/Y,D,Dx/Dy,Ms,Dims,Ex/Ey):-
        passable_tile(X/Y,Ms,Dims)
        ,maplist(ground,[X/Y,D,Dx/Dy,Ms])
	,Mv_x =.. [D,X,Dx]
	,Mv_y =.. [D,Y,Dy]
	,Ex is Mv_x
	,Ey is Mv_y
        ,passable_tile(Ex/Ey,Ms,Dims).



%!      passable_tiles(+Map,+Dimensions,-Tiles) is det.
%
%       Geneate a list of all passable Tiles in a Maze.
%
%       Map is the map of a maze given as a list of rows.
%
%       Dimensions is a pair Max_x - Max_y listing the limits of the two
%       map dimensions.
%
passable_tiles(Ms,Dims,Ts):-
        findall(X/Y
               ,passable_tile(X/Y,Ms,Dims)
               ,Ts).


%!      passable_tile(?Coordinates,+Map,+Dimensions) is det.
%
%       True for the Coordinates of a passable tile on a Map.
%
%       Coordinates is a pair X/Y, the x and y (column and row)
%       coordinates of a maze map.
%
%       Map is a list-of-lists, where each sub-list is a row of the map
%       (seen as a grid).
%
%       Dimensions is a pair Max_x - Max_y listing the limits of the two
%       map dimensions.
%
%       passable_tile/3 is true when the tile at the given X and Y are
%       marked as passalbe in the given Map.
%
%       Passable tiles are the ones defined in the predicate passable/1.
%
passable_tile(X/Y,Ms,Dims):-
        map_location(X/Y,T,Ms,Dims,true)
        ,passable(T).


%!      maze_dimensions(+Maze,-Max_x,-Max_y) is det.
%
%       Calculate the X and Y dimensions of a maze.
%
%       @tbd Not strictly necessary since the dimensions are in the
%       maze/3 atoms, but might be needed at some point so keep.
%
maze_dimensions([R1|Ms],Max_x,Max_y):-
        length([R1|Ms],Max_y)
        ,length(R1,Max_x).



%!       map_location(?Coordinates,?Tile,+Map,+Dimensions,+Rotate) is
%!       det.
%
%       Generate Coordinates of all Tiles in a Map.
%
%       Coordinates is a pair X/Y, representing coordinates of a Tile in
%       the Map.
%
%       Tile is the symbol of the terrain type at that Tile.
%
%       Map is the list of rows of a map.
%
%       Dimensions is a pair Max_x - Max_y listing the limits of the two
%       map dimensions.
%
%       Rotate is a boolean, either 'true' or 'false', denoting whether
%       the X/Y coordinates are to be rotated so that the origin of the
%       map is at the bottom-left corner.
%
map_location(Xt/Yt,T,Ms,Dims,true):-
        nth0(Y,Ms,Row)
        ,nth0(X,Row,T)
        ,rotation(X/Y,Dims,Xt/Yt).
map_location(X/Y,T,Ms,_Dims,false):-
        nth0(Y,Ms,Row)
        ,nth0(X,Row,T).



%!      start_location(+Map,+Dimensions,-Coords) is det.
%
%       The entry point in a Maze.
%
%       Dimensions is a pair Max_x - Max_y listing the limits of the two
%       map dimensions.
%
start_location(Ms,Dims,X/Y):-
        map_location(X/Y,s,Ms,Dims,true).



%!      end_location(+Map,+Dimensions,-Coords) is det.
%
%       The exit point in a Maze.
%
%       Dimensions is a pair Max_x - Max_y listing the limits of the two
%       map dimensions.
%
end_location(Ms,Dims,X/Y):-
        map_location(X/Y,e,Ms,Dims,true).



%!      rotation(+Coordinates,+Dims,-Rotated) is det.
%
%       Transform between list-based and Cartesian coordinates.
%
%       TODO: Document args.
%
%       Coordinates is a pair X/Y representing the x and y coordinates,
%       respectively, to be rotated.
%
%       Dimensions is a pair Max_x - Max_y listing the limits of the two
%       map dimensions.
%
%       Rotated is the pair X/Y transformed so that it is correct in a
%       Cartesian plan with the origin, 0/0, at the bottom-right corner.
%
%       This predicate is applied to the coordinates in a maze map given
%       as a list-of-lists, where each sub-list is a row of the map and
%       each element in a sub-list a tile in the map. The "natural"
%       (i.e. the easy) way to go through this list is by calling nth0/3
%       to find the n'th row, then nth0/3 again to find the n'th tile in
%       that row.
%
%       This "natural way" traverses the map from what is effectively
%       the top-left corner, meaning that the two calls to nth0/3 return
%       "0" as the index of the first element of the first sub-list. We
%       want to treat the maze as a Cartesian plane with the origin at
%       the bottom-left corner instead (because reasons; we may need to
%       calculate Euclidean distance, as a for instance) so this
%       predicate maps between the two representations by applying a
%       simple rotation to the input set of coordinates, to transform
%       them to proper Cartesian coordinates.
%
%       This predicate must be called by any predicate that inspects or
%       manipulates coordinates, e.g. the step_up/2 etc
%       primitive actions. Make sure to call it at the earliest point at
%       which a set of coordinates is encountered, to avoid code
%       duplication.
%
rotation(X/Y,_Mx-My,X/Yt):-
        Yt is (My - 1) - Y.
