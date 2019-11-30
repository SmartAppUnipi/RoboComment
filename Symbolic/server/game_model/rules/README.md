
# Files
- *rules.txt*: the actual file of rules parsed by the program
- *rules_guidelines.txt*: some tips on how to write rules
- *rules_future.txt*: ideas of future rules, but yet to be written correctly or tested
- *rules_to_debug.txt*: rules that are as correct as possibile, but yet to be tested or approved


# Grammar

* `.{0,N}` 
  
  Any subsequences from 0 to N
  
* `?`
  
  Only one event

* `*`
  
  Zero or more events

* `->` 
  
  Sequence operator

* `:` 
  
  This is used to impose conditions

* `!=` 
  
  Not equal

* `==` 
  
  Equal

* `___fx` 
  
  Internal functions

* `A in B` 
  
  Means that object A is within B

* `#var` 
  
  Used to refer to system variables

* `&` 
  
  AND operator

* `|` 
  
  OR operator


# Pragmatic

* `rule as @object`  
    > possession as @1


* `"rule_name" = rule(object)`
    > longBall = cross(t1) -> possession(p1)* -> cros(t1) : p1.team == t1
