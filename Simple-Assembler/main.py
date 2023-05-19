# list and dictionary containing data used for generating binary code
# dictionary containing opcode
import re
import sys

opcode = {'add': '00000', 'sub': '00001', 'mov': '00011', 'ld': '00100', 'st': '00101', 'mul': '00110',
          'div': '00111', 'xor': '01010', 'or': '01011', 'and': '01100', 'not': '01101', 'cmp': '01110', 'jmp': '01111',
          'jlt': '11100', 'jgt': '11101', 'je': '11111', 'hlt': '11010'}
opcodedollar = {'mov': '00010', 'rs': '01000', 'ls': '01001'}

# dictionary for type register
codetype = {'add': 'A', 'sub': 'A', 'mov': 'C', 'ld': 'D', 'st': 'D', 'mul': 'A',
            'div': 'C', 'xor': 'A', 'or': 'A', 'and': 'A', 'not': 'C', 'cmp': 'C', 'jmp': 'E',
            'jlt': 'E', 'jgt': 'E', 'je': 'E', 'hlt': 'F'}
codetypedollar = {'mov': 'B', 'rs': 'B', 'ls': 'B'}
register = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6': '110', 'FLAGS': '111'}
# other line might contain fault, var, label
# required list for codes
# checking not to be updated
checkerforlabel = ['jmp', 'jlt', 'jgt', 'je', 'hlt']

# codeline for type register
codeline = []
codelinewithopcode = []
codewithdollar = []
varline = []
labelline = []

# helping list and dictionary
label = []
faultyline = []
otherline = []
varcode = {}
labcode = {}
# type function for register
# Creating file for display
f = open('Display.txt', 'w')
f.close()


# function for writing contents in file


def filewriter(s):
    f = open('Display.txt', 'a')
    f.write(s)
    f.write("\n")
    f.close()

def assemblywriter(s):
    f = open('Assembler.txt', 'a')
    f.write(s)
    f.write("\n")
    f.close()

def is_binary(string):
    return re.match(r'^[01]+$', string) is not None


def varcreater(variableline):
    global codewithdollar, codelinewithopcode, varcode, labelline
    k = len(codewithdollar) + len(codelinewithopcode) + len(labelline) + len(faultyline)
    for i in variableline:
        j = i.split(' ')
        code = str(bin(k))[2:]
        if len(code) < 7:
            zero = (7 - len(code)) * str(0)
            s = zero
            s += code
        elif len(code) == 7:
            s = code
        else:
            s = "Invalid"
        varcode[j[1]] = s
        k += 1


def labelcreator():
    global label, labelline, codeline, codelinewithopcode, codewithdollar
    c = 0
    for i in codeline:
        j = i.split(':')
        if i in codelinewithopcode:
            c += 1
        elif i in codewithdollar:
            c += 1
        elif j[0] in label:
            t = 0
            # verifying label is it used as a variable
            for k in labelline:
                line = k.split(':')
                a = re.sub(r'^\s+', '', line[1])
                if j[0] == line[0]:
                    t += 1
            if t == 0 and (varcode.get(j[0][:-1]) is not None):
                labcode[j[0]] = 'variableusage'
            elif t == 0:
                labcode[j[0]] = 'general'
            elif t == 1:
                code = str(bin(c)[2:])
                if len(code) < 7:
                    zero = (7 - len(code)) * str(0)
                    s = zero
                    s += code
                elif len(code) == 7:
                    s = code
                else:
                    s = "Invalid"
                labcode[j[0]] = s
            else:
                labcode[j[0]] = 'toomanylabel'
            c += 1
        elif i in faultyline:
            c += 1


# this includes add, sub, mul ,xor, and ,or
def typeA(line):
    line1 = line.replace('\t', ' ')
    global varline, faultyline
    lineforA = line1.split(' ')
    if len(lineforA) != 4:
        s = 'General Syntax Error: Field does not contain sufficient number of elements'
        filewriter(s)
    else:
        if 'FLAGS' in line:
            # yes condition
            s = 'Syntax Error: Illegal use of Flag'
            filewriter(s)
        else:
            s = ''
            s += opcode.get(lineforA[0])
            s += '00'
            for i in range(1, 4):
                j = register.get(lineforA[i])
                if j is not None:
                    s += j
                else:
                    s += 'fault'
            if 'fault' in s:
                s = 'General Syntax Error: Field may contain labels or variables instead of registers'
                filewriter(s)
            else:
                filewriter(s)


# this includes mov, ls and rs
def typeB(line):
    line1 = line.replace('\t', ' ')
    lineforB = line1.split(' ')
    if len(lineforB) != 3:
        s = 'General Syntax Error: Field does not contain sufficient number of items'
        filewriter(s)
    else:
        if 'FLAGS' in line:
            # yes condition
            s = 'Syntax Error: Illegal use of Flag'
            filewriter(s)
        else:
            s = ''
            s += opcodedollar.get(lineforB[0])
            s += '0'
            # retrieving register value
            j = register.get(lineforB[1])
            if j is not None:
                s += j
            else:
                k = lineforB[1]
                if len(k) == 2 and (k[0] == 'R' or k[0] == 'r'):
                    s += 'invalidregister'
                else:
                    s += 'invalidcommand'

            # overflow condition for intermediate value

            try:
                val = int(lineforB[2][1:])
                fix = str(bin(val)[2:])
                if len(fix) > 7:
                    s += "overflow"
                elif len(fix) < 7:
                    s += '0' * (7 - len(fix))
                    s += fix
                else:
                    s += fix
            except ValueError:
                s += 'valueseemsincorrect'

            # file writing part
            if 'invalidregister' in s:
                s = 'Type Error: It seems you have typed incorrect register'
                filewriter(s)
            elif 'invalidcommand' in s:
                s = 'Type Error: Register is not recognized'
                filewriter(s)
            elif 'overflow' in s:
                s = 'Overflow :digit seem too large'
                filewriter(s)
            elif 'incorrect' in s:
                s = 'Value Error: immediate field contain more than number'
                filewriter(s)
            else:
                filewriter(s)


def typeC(line):
    line1 = line.replace('\t', ' ')
    lineforC = line1.split(' ')
    if len(lineforC) != 3:
        s = 'General Syntax Error: Field does not contain sufficient number of items'
        filewriter(s)
    else:
        if 'mov' == lineforC[0]:
            # yes condition
            s = opcode.get(lineforC[0])
            s += '00000'
            for i in range(1, 3):
                j = register.get(lineforC[i])
                if j is None:
                    s += 'invalidregister'
                else:
                    s += j
            if 'invalidregister' in s:
                s = 'Syntax Error: Invalid use of register'
                filewriter(s)
            else:
                filewriter(s)
        else:
            # no condition
            if 'FLAGS' in line:
                # yes condition
                s = 'Syntax Error: Illegal use of Flag'
                filewriter(s)
            else:
                # no condition
                s = opcode.get(lineforC[0])
                s += '00000'
                for i in range(1, 3):
                    j = register.get(lineforC[i])
                    if j is None:
                        s += 'invalidregister'
                    else:
                        s += j
                if 'invalidregister' in s:
                    s = 'Syntax Error: Invalid use of register'
                    filewriter(s)
                else:
                    filewriter(s)


def typeD(line):
    line1 = line.replace('\t', ' ')
    lineforD = line1.split(' ')
    if len(lineforD) != 3:
        s = 'General Syntax Error: Field does not contain sufficient number of items'
        filewriter(s)
    else:
        if 'FLAGS' in line:
            s = 'Syntax Error: Illegal use of flag'
            filewriter(s)
        else:
            s = opcode.get(lineforD[0])
            s += '0'
            j = register.get(lineforD[1])
            if j is None:
                s = 'Synatx Error: Register unable to find'
                filewriter(s)
            else:
                s += j

            k = varcode.get(lineforD[2])
            if k is None:
                s = f'Syntax Error : "{lineforD[2]}" variable does not exist'
                filewriter(s)
            elif k == 'Invalid':
                s = 'Syntax Error : code length is just large'
                filewriter(s)
            else:
                s += k
                filewriter(s)


def typeE(line):
    line1 = line.replace('\t', ' ')
    lineforE = line1.split(' ')
    if len(lineforE) != 2:
        s = 'General Syntax Error: Field does not contain sufficient number of items'
        filewriter(s)
    else:
        if 'FLAGS' in line:
            s = 'Syntax Error: Illegal use of flag'
            filewriter(s)
        else:
            s = opcode.get(lineforE[0])
            s += '0000'
            j = labcode.get(lineforE[1])
            if j is None:
                l = varcode.get(lineforE[1])
                if l is None:
                    s += 'labelabsent'
                else:
                    s += 'variableusage'
            else:
                s += j
            if 'labelabsent' in s:
                s = 'Syntax Error: label is not present'
                filewriter(s)
            elif 'variableusage' in s:
                s = 'Syntax Error: It seems that variable is used'
                filewriter(s)
            elif 'general' in s:
                s = 'General Syntax Error'
                filewriter(s)
            elif 'invalid' in s:
                s = 'Syntax Error: Code is too large'
                filewriter(s)
            elif 'toomanylabel' in s:
                s = 'Syntax Error: Single Label is assigned many values'
                filewriter(s)
            else:
                filewriter(s)


def typeF(line):
    line1 = line.replace('\t', ' ')
    lineforF = line1.split(' ')
    if len(lineforF) != 1:
        s = 'General Syntax Error: Field does not contain sufficient number of items'
        filewriter(s)
    else:
        s = opcode.get(lineforF[0])
        s += '0' * 11
        filewriter(s)


# Taking input and storing it in Assembler
lines = sys.stdin.readlines()
f = open('Assembler.txt','w')
f.close()
for i in lines:
    assemblywriter(i)
    
# file management
Assembler = open('Assembler.txt', 'r')
a = Assembler.readlines()

# storing assembly code in codeline list
for i in a:
    old = i.replace('\n', '')
    if len(old) != 0:
        codeline.append(old)

non_var = 0
# taking care of all the cases except of label line and faulty line
for i in codeline:
    a = i.split(' ')
    if ('$' in i) and (a[0] in opcodedollar.keys()):
        codewithdollar.append(i)
        non_var += 1
    elif a[0] in opcode.keys():
        codelinewithopcode.append(i)
        non_var += 1
    elif a[0] == 'var' and (len(a) == 2):
        if non_var != 0:
            pass
        else:
            varline.append(i)
    else:
        otherline.append(i)
        non_var += 1
    if (a[0] in checkerforlabel) and (len(a) == 2):
        label.append(a[1])

# taking care for label line and faulty line
for i in otherline:
    a = i.split(': ')
    if a[0] in label:
        labelline.append(i)
    else:
        if len(a) == 2:
            label.append(a[0])
            labelline.append(i)
        else:
            faultyline.append(i)
varcreater(varline)
labelcreator()
result = -1

# label correction
for i in range(len(codeline)):
    if codeline[i] in codelinewithopcode:
        splitter = codeline[i].split(' ')
        t = codetype.get(splitter[0])
        if t == 'A':
            pass
        elif t == 'B':
            pass
        elif t == 'C':
            pass
        elif t == 'D':
            pass
        elif t == 'E':
            pass
        elif t == 'F':
            pass
            result = i
            break
    elif codeline[i] in codewithdollar:
        pass
    elif codeline[i] in labelline:
        j = codeline[i].split(':')
        p = re.sub(r'^\s+', '', j[1])
        splitter = p.split(' ')
        if '$' in codeline[i]:
            t = codetypedollar.get(splitter[0])
        else:
            t = codetype.get(splitter[0])
        if t == 'A':
            pass
        elif t == 'B':
            pass
        elif t == 'C':
            pass
        elif t == 'D':
            pass
        elif t == 'E':
            pass
        elif t == 'F':
            result = i
            break

    elif codeline[i] in faultyline:
        if codeline[i][0] == " ":
            a = re.sub(r'^\s+', '', codeline[i])
            splitter = a.split(' ')
            t = codetype.get(splitter[0])
            if t == 'E':
                label.append(a.split(" ")[1])
                labelcreator()
            elif t == 'F':
                result = i
                break
        elif ":" in codeline[i]:
            if i not in labelline:
                labelline.append(codeline[i])
            newline = codeline[i].split(":")[1]
            a = re.sub(r'^\s+', '', newline)
            splitter = a.split(' ')
            t = codetype.get(splitter[0])
            if t == 'E':
                label.append(a.split(" ")[1])
                labelcreator()
            elif t == 'F':
                break

# demo testing end
for i in range(len(codeline)):
    if codeline[i] in codelinewithopcode:
        splitter = codeline[i].split(' ')
        t = codetype.get(splitter[0])
        if t == 'A':
            typeA(codeline[i])
        elif t == 'B':
            typeB(codeline[i])
        elif t == 'C':
            typeC(codeline[i])
        elif t == 'D':
            typeD(codeline[i])
        elif t == 'E':
            typeE(codeline[i])
        elif t == 'F':
            typeF(codeline[i])
            result = i
            break
    elif codeline[i] in codewithdollar:
        typeB(codeline[i])
    elif codeline[i] in labelline:
        j = codeline[i].split(':')
        p = re.sub(r'^\s+', '', j[1])
        splitter = p.split(' ')
        if '$' in codeline[i]:
            t = codetypedollar.get(splitter[0])
        else:
            t = codetype.get(splitter[0])
        if t == 'A':
            typeA(p)
        elif t == 'B':
            typeB(p)
        elif t == 'C':
            typeC(p)
        elif t == 'D':
            typeD(p)
        elif t == 'E':
            typeE(p)
        elif t == 'F':
            typeF(p)
            result = i
            break
    elif codeline[i].split(" ")[0] == 'var' and len(codeline[i].split(" ")) == 2:
        a = varcode.get(codeline[i].split(" ")[1])
        if a is None:
            s = "Syntax Error: Variable should be declared at the beginning"
            filewriter(s)
    elif codeline[i] in faultyline:
        if codeline[i][0] == " ":
            a = re.sub(r'^\s+', '', codeline[i])
            splitter = a.split(' ')
            if '$' in codeline[i]:
                t = codetypedollar.get(splitter[0])
            else:
                t = codetype.get(splitter[0])
            if t == 'A':
                typeA(a)
            elif t == 'B':
                typeB(a)
            elif t == 'C':
                typeC(a)
            elif t == 'D':
                typeD(a)
            elif t == 'E':
                label.append(a.split(" ")[1])
                labelcreator()
                typeE(a)
            elif t == 'F':
                typeF(a)
                result = i
                break
        elif ":" in faultyline:
            if i not in labelline:
                labelline.append(codeline[i])
            newline = codeline[i].split(":")[1]
            a = re.sub(r'^\s+', '', newline)
            splitter = a.split(' ')
            if '$' in codeline[i]:
                t = codetypedollar.get(splitter[0])
            else:
                t = codetype.get(splitter[0])
            if t == 'A':
                typeA(a)
            elif t == 'B':
                typeB(a)
            elif t == 'C':
                typeC(a)
            elif t == 'D':
                typeD(a)
            elif t == 'E':
                label.append(a.split(" ")[1])
                labelcreator()
                typeE(a)
            elif t == 'F':
                typeF(a)
                result = i
                break
        else:
            line1 = codeline[i].replace('\t', ' ')
            a = re.sub(r'^\s+', '', line1)
            splitter = a.split(' ')
            if '$' in codeline[i]:
                t = codetypedollar.get(splitter[0])
            else:
                t = codetype.get(splitter[0])
            if t == 'A':
                typeA(a)
            elif t == 'B':
                typeB(a)
            elif t == 'C':
                typeC(a)
            elif t == 'D':
                typeD(a)
            elif t == 'E':
                label.append(a.split(" ")[1])
                labelcreator()
                typeE(a)
            elif t == 'F':
                typeF(a)
                result = i
                break
            else:
                s = f'General Syntax Error: var "{codeline[i]}" is not present'
                filewriter(s)

c = 0
for i in codeline:
    a = i.split(" ")
    if 'hlt' in a:
        c += 1

if c == 0:
    s = "General Syntax Error: hlt not present"
    filewriter(s)

if result != (len(codeline) - 1):
    s = "Syntax Error :Can't execute lines after hlt"
    filewriter(s)

binaryline = []
errorline = []

f = open('Display.txt', 'r')
for j in f.readlines():
    i = j.replace("\n", "")
    if is_binary(i):
        binaryline.append(i)
    else:
        errorline.append(i)

f.close()
if len(errorline) == 0:
    for i in binaryline:
        print(i)
else:
    print(errorline[0], end="")
