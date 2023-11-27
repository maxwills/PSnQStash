import bdb
import inspect
from time import sleep
from random import random
from threading import Thread
from threading import Lock
from threading import Condition
import linecache
import dis
import ast

class ScriptableBdb(bdb.Bdb):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.finished = False
        self.condition = Condition()
        self.currentFrame = None
        self.shouldYield = False
        self.startingFilename = ""
        self.currentStepNumber = 0
        self.isMethodCallFlag = False
        self.isMethodReturnFlag = False
        self.callNodeDetectedFlag=False

    def user_line(self, frame):
        self.set_step()
        while self.shouldYield:
            self.condition.wait()
        self.currentFrame = frame
        #print('user_line called')
        self.shouldYield = True
        self.callNodeDetectedFlag = bool(self.collect_call_nodes(self.currentNode()))
        self.currentStepNumber = self.currentStepNumber + 1
        self.condition.notify()
        # self.set_step()
    
    def currentLineNumber(self):
        return self.currentFrame.f_lineno

    def user_call(self, frame, argument_list):
        while self.shouldYield:
            self.condition.wait()
        self.currentFrame = frame
        self.isMethodCallFlag = True
        self.shouldYield = True
        self.currentStepNumber = self.currentStepNumber + 1
        self.condition.notify()

    def user_return(self, frame, returnVal):
        while self.shouldYield:
            self.condition.wait()
        self.currentFrame = frame
        self.isMethodReturnFlag=True
        self.shouldYield = True
        self.currentStepNumber = self.currentStepNumber + 1
        self.condition.notify()

    def user_exception(self, frame, exc_info):
        while self.shouldYield:
            self.condition.wait()
        self.currentFrame = frame
        self.shouldYield = True
        self.currentStepNumber = self.currentStepNumber + 1
        self.condition.notify()

    def executeProgram(self):
        with self.condition:
            with open(self.startingFilename, 'r') as f:
                script = f.read()
            self.set_break(self.startingFilename, 0)
            self.run(script)
            self.finished=True
            self.condition.notify()

    def isMethodCall(self):
        if self.currentFrame == None:
            return False
        node = self.currentNode()
        if isinstance(node, ast.ClassDef):
            return False
        return self.currentOpIsCall()
    
    def collect_call_nodes(self, node):
        nodes = []
        if node is None:
            return nodes
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name): #and node.func.id == "print":
            nodes.append(node)
          
        for child_node in ast.iter_child_nodes(node):
            nodes.extend(self.collect_call_nodes(child_node))
        return nodes

    def currentOpIsCall(self):
        call_ops = [131,141,142,161]
        return self.currentOp() in call_ops
    
    def currentNode(self):
        frame= self.currentFrame
        line = inspect.getframeinfo(frame).lineno
        with open(self.currentFilename()) as fin:
            parsed = ast.parse(fin.read())
        for node in ast.walk(parsed):
            if (isinstance(node, ast.stmt) or isinstance(node, ast.expr)) and node.lineno == line:
                return node
                
        return None
        
    def isAssignment(self):
        return isinstance(self.currentNode(), ast.Assign) and not self.isMethodReturnFlag and not self.currentOpIsCall()

    def stepNumber(self):
        return self.currentStepNumber

    def currentFilename(self):
        filename = self.currentFrame.f_code.co_filename
        if filename == '<string>':
            return self.startingFilename
        return filename

    def currentLine(self):
        lineno = self.currentFrame.f_lineno
        filename = self.currentFilename()
        line = linecache.getline(filename, lineno)
        return  line.strip()
    
    def currentOp(self):
        return self.currentFrame.f_code.co_code[self.currentFrame.f_lasti]
        
    def currentBytecode(self):
        frame = self.currentFrame
        bytecode = frame.f_code.co_code
        instruction_offset = frame.f_lasti
        # Disassemble the bytecode and retrieve the next instruction
        instructions = dis.Bytecode(bytecode)
        for instruction in instructions:
            if instruction.offset > instruction_offset:
                return instruction
        # defaults to the last instruction, if this happens at all
        return frame.f_code.co_code[frame.f_lasti]

    def getShouldExcludeCall(self):
        if self.lastFlagedLine == self.currentLineNumber():
            return True
        return False




