from twisted.internet import protocol, reactor, endpoints, threads, defer
import cmd, json, time

"""Client Protocol Class"""
class DataTransport(protocol.Protocol):
    def __init__(self, msg):
        self.msg = msg
        self.done = defer.Deferred()

    def connectionMade(self):
        self.transport.write(json.dumps(self.msg).encode("utf-8"))

    def dataReceived(self, data):
        response = json.loads(data.decode("utf-8").strip())["response"]
        self.done.callback(response)        
    
"""Cmd Module Class"""
class UserCLI(cmd.Cmd):
    prompt = "(callcenter) > "

    """Make connection and send message to the endpoint, them wait for response"""
    def sendMessage(self, command, id):
        point = endpoints.TCP4ClientEndpoint(reactor, "localhost", 5678)
        protocol = DataTransport({"command": command, "id": id})
        d = endpoints.connectProtocol(point, protocol)

        def waitResponse(protocol):
            return protocol.done
        
        d.addCallback(waitResponse)
        return d

    """Quits Application"""
    def do_quit(self, arg):
        reactor.callFromThread(reactor.stop)
        return True
        
    """Makes application receive a call whose id is <id>"""
    def do_call(self, arg):
        print(threads.blockingCallFromThread(reactor, self.sendMessage, "call", arg))

    """Makes operator <id> answer a call being delivered to it."""
    def do_answer(self, arg):
        print(threads.blockingCallFromThread(reactor, self.sendMessage, "answer", arg))

    """Makes operator <id> reject a call being delivered to it."""
    def do_reject(self, arg):
        print(threads.blockingCallFromThread(reactor, self.sendMessage, "reject", arg))

    """Makes call whose id is <id> be finished."""
    def do_hangup(self, arg):
        print(threads.blockingCallFromThread(reactor, self.sendMessage, "hangup", arg))

reactor.callInThread(UserCLI().cmdloop)
reactor.run()