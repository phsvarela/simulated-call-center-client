import cmd 

"""Globals"""
available = "avaiable"
ringing = "ringing"
busy = "busy"

"""Operator Class"""
class Operator:
    """Operator starts available"""
    def __init__(self, id):
        self.id = id
        self.state = available
        self.idCall = None

"""Queue Class"""
class Queue:
    def __init__(self):
        self.items = []
        self.frontIdx = 0

    def _compress(self):
        l = []
        for i in range(self.frontIdx, len(self.items)):
            l.append(self.items[i])
        
        self.items = l
        self.frontIdx = 0

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.frontIdx * 2 > len(self.items):
            self._compress()

        item = self.items[self.frontIdx]
        self.frontIdx += 1
        return item
    
    def __len__(self):
        return len(self.items)

    """Returns true if pointers is not at the end of the queue"""
    def __bool__(self):
        return self.frontIdx < len(self.items)

"""Call Center Queue Manager Class"""
class CallCenter:
    def __init__(self):
       self.queue = Queue()
       self.operators = [Operator("A"), Operator("B")]

    """Deliver call to operator"""
    def __deliverCall(self, call, operator):
        operator.state = ringing
        operator.idCall = call
        print(f"Call {call} ringing for operator {operator.id}")

    """Search for the operator using the id"""
    def __searchOperatorById(self, id):
        for op in self.operators:
            if op.id == id:
                return op
            
        return None

    """Search for the operator using the call"""
    def __searchOperatorByIdCall(self, idCall):
        for op in self.operators:
            if op.idCall == idCall:
                return op
            
        return None
    
    """Search for another operator"""
    def __searchAvailableOperator(self):
        for op in self.operators:
            if op.state == available:
                return op
            
        return None

    """Call routine"""
    def call(self, arg):
        print(f"Call {arg} received")

        """Deliver the call for the next available operator"""
        operator = self.__searchAvailableOperator()
        if operator != None:
            self.__deliverCall(arg, operator)
            return

        """If there are no available operators, then put the call in the end of the queue"""
        self.queue.enqueue(arg)
        print(f"Call {arg} waiting in queue")
        
    """Answer routine"""
    def answer(self, arg):        
        operator = self.__searchOperatorById(arg)

        """Operator answer the call and change state"""
        if operator != None:
            operator.state = busy
            print(f"Call {operator.idCall} answered by operator {operator.id}")

    """Reject routine"""
    def reject(self, arg):
        operator = self.__searchOperatorById(arg)

        """Operator reject call and change state, then take the next call in queue"""
        if operator != None:
            call = operator.idCall
            operator.state = available
            operator.idCall = None
            print(f"Call {call} rejected by operator {operator.id}")
            self.queue.enqueue(call)

            if self.queue:
                self.__deliverCall(self.queue.dequeue(), self.__searchAvailableOperator())

    """Hangup routine"""
    def hangup(self, arg):
        operator = self.__searchOperatorByIdCall(arg)

        """Operator hangup call and change state, then take the next call in queue"""
        if operator != None:
            
            if operator.state == ringing:
                print(f"Call {arg} missed")
            else:
                print(f"Call {arg} finished and operator {operator.id} available")

            operator.state = available
            operator.idCall = None

            if self.queue:
                self.__deliverCall(self.queue.dequeue(), operator)
        else:
            """Call hanguped without being delivered or answered, then removed from the queue"""
            print(f"Call {arg} missed")
            self.queue.dequeue()

"""Cmd Module Class"""
class MyCommand(cmd.Cmd):
    prompt = "(callcenter) > "

    def __init__(self):
        super().__init__()
        self.callCenterInstance = CallCenter()

    def do_quit(self, arg):
        """Quits Application"""
        return True
        
    def do_call(self, arg):
        """Makes application receive a call whose id is <id>"""
        self.callCenterInstance.call(arg)

    def do_answer(self, arg):
        """Makes operator <id> answer a call being delivered to it."""
        self.callCenterInstance.answer(arg)

    def do_reject(self, arg):
        """Makes operator <id> reject a call being delivered to it."""
        self.callCenterInstance.reject(arg)

    def do_hangup(self, arg):
        """Makes call whose id is <id> be finished."""
        self.callCenterInstance.hangup(arg)

MyCommand().cmdloop()