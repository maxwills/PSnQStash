from psnq import ProgramStates
from psnq import CurrentState

debuggee_program_filename ='debuggee_program.py'

print('I. Calls query:\n')
ps = ProgramStates.fromProgramFile(debuggee_program_filename)
calls = [{'method':state.methodCallName(), 
          'stack':state.formattedStackPath()} 
         for state in ps if state.isMethodCall()]
for c in calls:
    print(c['method'] + ' # Called from: '+ c['stack']  )

print('\nII. Assignments query:\n')
ps = ProgramStates.fromProgramFile(debuggee_program_filename)
assignments = [{'assign':state.assignmentCode(), 
                'stack':state.formattedStackPath()} 
               for state in ps if state.isAssignment()]
for a in assignments:
    print(a['assign'] + ' # Called from: '+ a['stack']  )