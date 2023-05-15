# CO-project
It defines dictionaries for opcodes, opcode variations, code types, and registers.

It defines empty lists to store different types of code lines.

It defines helper lists and dictionaries for labels, faulty lines, variables, and labels with code.

It defines a file writer function to write the generated binary code to a file called "Display.txt".

It defines functions for different types of instructions (A, B, C, D, E, F) to generate binary code based on the provided assembly-like instructions.

It reads the "Assembler.txt" file and stores each non-empty line in the codeline list.

It categorizes the code lines into opcode lines, opcode variations with a dollar sign, variable lines, and other lines.

It creates variables from the varline list and labels from the labelline list.

It iterates over the codeline list and calls the respective type function based on the opcode or label present in the line.

It writes the generated binary code to the "Display.txt" file.
