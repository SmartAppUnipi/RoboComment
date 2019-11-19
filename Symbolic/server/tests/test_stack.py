from game_model.stack import Stack,EmptyQueueError,InvalidIndexError,NotFoundElementError
import pytest

def test_new_empty_stack():
     stack = Stack()
     assert len(stack.get_stack()) == 0

def test_insert_one_element():
     stack = Stack()
     stack.push("a",0)
     assert len(stack.get_stack()) == 1
     assert list(stack.get_stack()) == ['a']

def test_insert_multiple_elements():
     stack = Stack()
     stack.push('a',0)
     stack.push('b',1)
     stack.push('c',1)
     assert stack.get_stack() == ['a','c','b']

def test_push_front():
     stack = Stack()
     stack.push_front('a')
     stack.push_front('b')
     stack.push_front('c')
     assert stack.get_stack() == ['c','b','a']

def test_get_element():
     stack = Stack()
     stack.push('a',0)
     stack.push('b',1)
     stack.push('c',2)
     elem = stack.get(1)
     assert elem == 'b'

def test_size():
     stack = Stack()
     assert stack.size() == 0
     stack.push('a',0)
     stack.push('b',1)
     stack.push('c',2)
     assert stack.size() == 3
     stack.pop_front()
     assert stack.size() == 2
     stack.pop_front()
     stack.pop_front()
     assert stack.size() == 0

def test_duplicate():
      stack = Stack()
      stack.push('a',0)
      stack.push('b',1)
      stack.push('c',2)
      stack_dup = stack.duplicate()
      assert stack_dup.size() == stack.size()
      assert stack_dup.get_stack() == stack.get_stack()

def test_pop():
     stack = Stack()
     with pytest.raises(EmptyQueueError):
          stack.pop(0)

     stack.push('a',0)
     with pytest.raises(InvalidIndexError) as e:
          stack.pop(1)
     assert str(e.value) == "'The element at index 1 does not exist'"
     
     assert stack.pop(0) == 'a'

     with pytest.raises(EmptyQueueError) as e:
          stack.pop(0)
     assert str(e.value) ==  "'The queue is empty'"
     

     stack.push_front('b')
     stack.push_front('c')
     stack.push_front('d')
     assert stack.pop(1) == 'c'
     assert stack.get_stack() == ['d','b']

def test_pop_front():
     stack = Stack()
     with pytest.raises(EmptyQueueError):
          stack.pop_front()

     stack.push('a',0)     
     assert stack.pop_front() == 'a'
     
     with pytest.raises(EmptyQueueError):
          stack.pop(0)
     
     stack.push_front('b')
     stack.push_front('c')
     stack.push_front('d')
     assert stack.pop_front() == 'd'


def test_clear():
     stack = Stack()
     stack.clear()
     assert stack.size() == 0

     stack.push_front('b')
     stack.push_front('c')
     stack.push_front('d')

     stack.clear()
     assert stack.size() == 0
     assert stack.get_stack() == []


def test_find_element():
     stack = Stack()

     with pytest.raises(NotFoundElementError) as e:
          stack.find('v')
     
     assert str(e.value) == "'The element is not in the stack'"
     
     stack.push_front('a')
     stack.push_front('b')
     stack.push_front('c')
     stack.push_front('d')

     assert stack.find('c') == 1
     assert stack.find('d') == 0
     assert stack.find('a') == 3

     with pytest.raises(NotFoundElementError) as e:
          stack.find('v')
     
     stack.pop_front()
     with pytest.raises(NotFoundElementError) as e:
          stack.find('d')
     