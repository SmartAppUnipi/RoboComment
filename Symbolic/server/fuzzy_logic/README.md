# Fuzzy Logic

In this folder those files are provided:
- **fuzzy_set.py**: provides the implementation of a fuzzy set: provides the possibility to define a fuzzy set (I.E. men height), some membership functions (I.E. tall, short, average...) and provides operations like union, intersection, containment, membership function evaluation (with modifiers like 'very', 'somewhat'...) and some graphical plots to be used in the debugging phase to make sure no mistakes were made in function definition
- **membership_function**: file used by fuzzy_set.py, it models a fuzzy function over a generic domain.

## Modifiers
The provided modifiers are: 
- *a little*
- *slightly*
- *very*
- *extremely*
- *very very*
- *more or less*
- *somewhat*

## Fuzzy Set Example

    fs = FuzzySet(140, 210, 1, universe_descr="Height in cm")
    fs.new_membership_func("Short", 170, 160)
    fs.new_membership_func("Tall", 170, 190)
    fs.new_membership_func("Avg", 160, 175, 190)
    fs.plot_membership("Tall", 'very')
    fs.plot_membership("Short")
    fs.plot_membership("Avg", 'somewhat')
    interc = fs.intersection('Tall', 'Avg')
    fs.new_membership_func_from_list(interc, "tall INTERSECTION average")
    fs.plot_membership("tall INTERSECTION average")
    union = fs.union('Short', 'Avg', a_modifier='extremely')
    fs.new_membership_func_from_list(interc, "extremely short UNION avg")
    fs.plot_membership("extremely short UNION avg")
    print(fs.find_strongest_modifier(185, 'Tall', 0.8))
    print(fs.find_strongest_modifier(165, 'Short', 0.6))
