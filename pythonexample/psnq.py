from time import sleep
from random import random
from threading import Thread
from threading import Condition
from debugger import ScriptableBdb
import inspect 

class CurrentState:
    def __init__(self):
        self._debugger = None

    def isMethodCall(self):
        return self._debugger.isMethodCall()

    def isAssignment(self):
        return self._debugger.isAssignment()

    def node(self):
        return  self._debugger.currentNode()

    def methodCallName(self):
        return self._debugger.currentLine()
    
    def assignmentCode(self):
        return self._debugger.currentLine()
    
    def currentLineOfCode(self):
        return self._debugger.currentLine()
    
    def stackPath(self):
        # the current frame goes first, last frame is the first caller
        frame = self.currentFrame()
        stack = inspect.getouterframes(frame)
        # Extract class names from the stack
        path = [
            (frame_info.frame.f_locals.get('self', None).__class__.__name__, frame_info.frame.f_code.co_name)
            for frame_info in stack
        ]
        # filter out frames unrelated to the debuggee
        index = path.index(('NoneType','<module>'))
        return path[:index+1:]
    
    def formattedStackPath(self):
        return " / ".join(list([ (str(c[0])+" >> "+str(c[1])) for c in self.stackPath()[::-1]]))
    
    def currentFrame(self):
        return self._debugger.currentFrame
        

class ProgramStates:
    def fromProgramFile(pythonFilePath):
        # To yield program states, we need to interrupt the execution of the debugger at each step hook.
        debugger = ScriptableBdb()
        debugger.startingFilename = pythonFilePath
        currentState = CurrentState()
        currentState._debugger = debugger
        worker = Thread(target=debugger.executeProgram)
        worker.start()
        with debugger.condition:
            while not debugger.finished:
                while not debugger.shouldYield and not debugger.finished:
                    debugger.condition.wait()
                if debugger.shouldYield:
                    yield currentState
                debugger.isMethodReturnFlag=False
                debugger.isMethodCallFlag = False
                debugger.callNodeDetectedFlag=False
                debugger.shouldYield = False
                debugger.condition.notify()




