import sys
import os
import re
import ast

# print(sys.argv)
# if len(sys.argv) < 1:
#     print("Not enough arguments passed for the program to function.")

args = sys.argv


# args = ["code_analyzer.py", "D:\\Python\\PycharmProjects\\test\\manualtestcases"]


def length_check(line, i, path):
    if len(line[:-1]) > 79:
        print(f"{path}: Line {i + 1}: S001 Too long")


def indentation_check(line, i, path):
    for j in range(0, len(line)):
        if line[j] != " ":
            break
    if j % 4 != 0:
        print(f"{path}: Line {i + 1}: S002 Indentation is not a multiple of four")


def colon_check(line, i, path):
    if "#" in line:
        statement = line.split("#")
        line = statement[0].replace(" ", "")
    line = line.replace("\n", "")
    if line.endswith(";"):
        print(f"{path}: Line {i + 1}: S003 Unnecessary semicolon after a statement;")


def in_line_comment_check(line, i, path):
    if line[0] == "#" or "#" not in line:
        return
    statement = line.split("#")[0]
    count = 0
    for char in statement[::-1]:
        if char != " ":
            break
        count += 1
    if count < 2:
        print(f"{path}: Line {i + 1}: S004 Less than two spaces before inline comments")


def todo_check(line, i, path):
    if "#" not in line:
        return
    comment = line.split("#")[-1]
    if 'TODO' in comment.upper():
        print(f"{path}: Line {i + 1}: S005 TODO found")


def blank_line_check(blank_lines, i, path):
    if blank_lines > 2:
        print(f"{path}: Line {i + 1}: S006 More than two blank lines preceding a code line")
    return 0


def construction_name_check(line, i, path):
    template = "^\s{0,}(class|def)\s\s+"
    template_class = "^\s{0,}class [a-z]"
    template_def = "^\s{0,}def [A-Z]"
    if re.match(template, line):
        print(f"{path}: Line {i + 1}: S007 Too many spaces after (def or class)")
    if re.match(template_class, line):
        print(f"{path}: Line {i + 1}: S008 Class name should be written in CamelCase")
    if re.match(template_def, line):
        print(f"{path}: Line {i + 1}: S009 Function name should be written in snake_case")


def arguments_check(i, path):
    data = open(path).read()
    tree = ast.parse(data)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.lineno == i + 1:
            template_arg = "^[A-Z]"
            arguments = node.args.args
            for arg in arguments:
                if re.match(template_arg, arg.arg):
                    print(f"{path}: Line {i + 1}: S010 Argument name {arg.arg} should be written in snake_case")


def variable_check(i, path):
    data = open(path).read()
    tree = ast.parse(data)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and node.lineno == i + 1:
            template_var = "^[A-Z]"
            variable_name = node.id
            # print(path, f"line{i+1}", variable_name)
            if re.match(template_var, variable_name):
                print(f"{path}: Line {i + 1}: S011 Argument name {variable_name} should be written in snake_case")


def deafult_arg_val_check(i, path):
    data = open(path).read()
    tree = ast.parse(data)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.lineno == i + 1:
            for item in node.args.defaults:
                # print(item)
                if isinstance(item, ast.List):
                    print(f"{path}: Line {i + 1}: S012 The default argument value is mutable.")


def code_analyzer(lines, path):
    blank_lines = 0
    for i in range(0, len(lines)):
        if lines[i] != "\n":
            length_check(lines[i], i, path)
            indentation_check(lines[i], i, path)
            colon_check(lines[i], i, path)
            in_line_comment_check(lines[i], i, path)
            todo_check(lines[i], i, path)
            blank_lines = blank_line_check(blank_lines, i, path)
            construction_name_check(lines[i], i, path)
            arguments_check(i, path)
            variable_check(i, path)
            deafult_arg_val_check(i, path)
        else:
            blank_lines += 1


if args[1].endswith(".py"):
    with open(args[1]) as file:
        lines_list = file.readlines()
    path = args[1]
    code_analyzer(lines_list, path)
else:
    list_of_files = os.listdir(args[1])
    for subfile in list_of_files:
        if subfile.endswith(".py"):
            with open(f"{args[1]}\\{subfile}") as file:
                lines_list = file.readlines()
            path = f"{args[1]}\\{subfile}"
            code_analyzer(lines_list, path)
