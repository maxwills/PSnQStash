# PSnQStash
Code for the PSnQ.

The proto-draft of the paper is here: [gitlab inria](https://gitlab.inria.fr/RMODPapers/maxw/2023-maxw-phd/-/tree/master/Chapters/chapter-pnq-system?ref_type=heads)

## Python Example
Download the folder with the example.
To run it, do `python runexample.py` in a terminal.

## C# Example
The C# example is only available at the moment in the artifact (check your work or personal email for the link).

## Pharo Example
The Pharo example requires SeekerDebugger to run.

Requires the following classes and methods:

```Smalltalk
MyClass >> methodA
   | w |
   w := 1.
   ^ w
MyClass >> methodB
   | x |
   x := 2.
   self methodC.
   ^ x
MyClass >> methodC
   | y |
   y := 3.
   ^ y
MyClass >> methodD
   | z |
   z := 4.
   ^ z

Program class >> main
   | obj |
   obj := MyClass 
      new.
   obj methodA.
   obj methodB.
   obj methodD
```

To run the first example in Pharo, do the following in a Playground:

```Smalltalk
Transcript show: 'I. Message sends query (Pharo)'; cr.
debuggeeProgramBlock := [ Program main ].
ps := debuggeeProgramBlock asProgramStates.
messageSends := Query from: ps
  select: [ :state | state isMessageSend ]
  collect: [ :state | {(#method −> state messageMethodName). (#stack −> state formattedStack)}
    asDictionary].
assignments do: [ :a | Transcript show: (a at: #method) , ' "Called in: ' , (a at: #stack) , '"'; cr ]
```

To run the second example in Pharo, do the following in a Playground:

```Smalltalk
Transcript show: 'II. Assignments query (Pharo):'; cr.
debuggeeProgramBlock := [ Program main ].
ps := debuggeeProgramBlock asProgramStates.
assignments := Query from: ps
   select: [ :state | state isAssignment ]
   collect: [ :state | {(#code -> state expressionCode). (#stack -> state formattedStack)} asDictionary].
assignments do: [ :a | Transcript show: (a at: #code) , ' "Called in: ' , (a at: #stack) , '"'; cr ]
```
