from consume import consume
from matchOwner import matchOwner

##{Owner}{Vacant}*{Owner}
def matchPass(stack):
    first = stack.pop() #Consume first element
    if not matchOwner(first):       #Check first owner
        return False
    while True:
        second = stack.pop()
        if matchOwner(second):
            break
    #return match(first.team, second.team)
    raise NotImplementedError   #ToDo need to import matcher