import tika
from tika import parser
import os
tika.initVM()


IS_worksheet_directory = r"C:\Users\patel\Downloads\COMP6741_P1_G7\COMP6741_P1\University\COMP6741\Worksheets"
AI_worksheet_directory = r"C:\Users\patel\Downloads\COMP6741_P1_G7\COMP6741_P1\University\COMP6721\Worksheets"
IS_Save_worksheet_directory = r"C:\Users\patel\Downloads\COMP6741_P1_G7\COMP6741_P1\TextConvert\COMP6741\worksheet"
AI_Save_worksheet_directory = r"C:\Users\patel\Downloads\COMP6741_P1_G7\COMP6741_P1\TextConvert\COMP6721\worksheet"

IS_lab_directory = r"C:\Users\patel\Downloads\COMP6741_P1_G7\COMP6741_P1\University\COMP6741\Labs"
AI_lab_directory = r"C:\Users\patel\Downloads\COMP6741_P1_G7\COMP6741_P1\University\COMP6721\Labs"
IS_Save_lab_directory = r"C:\Users\patel\Downloads\COMP6741_P1_G7\COMP6741_P1\TextConvert\COMP6741\Labs"
AI_Save_lab_directory = r"C:\Users\patel\Downloads\COMP6741_P1_G7\COMP6741_P1\TextConvert\COMP6721\Labs"

IS_lecture_directory = r"C:\Users\patel\Downloads\COMP6741_P1_G7\COMP6741_P1\University\COMP6741\Lectures"
AI_lecture_directory = r"C:\Users\patel\Downloads\COMP6741_P1_G7\COMP6741_P1\University\COMP6721\Lectures"
IS_Save_lecture_directory = r"C:\Users\patel\Downloads\COMP6741_P1_G7\COMP6741_P1\TextConvert\COMP6741\lecture"
AI_Save_lecture_directory = r"C:\Users\patel\Downloads\COMP6741_P1_G7\COMP6741_P1\TextConvert\COMP6721\lecture"

i=1
print("---------------------------Intelligent System-------------------------------")
for file in os.listdir(IS_worksheet_directory):
    print(file)
    parsedfile = parser.from_file(IS_worksheet_directory + "\\" + file)
    f = open(IS_Save_worksheet_directory + '\\worksheet' + str(i) + '.txt', 'w', encoding='UTF-8')
    file_string_with_blank_lines = parsedfile["content"].strip()
    lines = file_string_with_blank_lines.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    file_string_without_empty_lines = ""
    lines_seen = set()
    for line in non_empty_lines:
        if line not in lines_seen: # not a duplicate
            file_string_without_empty_lines += line.strip() + "\n"
            lines_seen.add(line)
    f.write(file_string_without_empty_lines)
    f.close()
    i=i+1

i=1
for file in os.listdir(IS_lecture_directory):
    print(file)
    parsedfile = parser.from_file(IS_lecture_directory + "\\" + file)
    f = open(IS_Save_lecture_directory + '\\slide' + str(i) + '.txt', 'w', encoding='UTF-8')
    file_string_with_blank_lines = parsedfile["content"].strip()
    lines = file_string_with_blank_lines.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    file_string_without_empty_lines = ""
    lines_seen = set()
    for line in non_empty_lines:
        if line not in lines_seen: # not a duplicate
            file_string_without_empty_lines += line.strip() + "\n"
            lines_seen.add(line)
    f.write(file_string_without_empty_lines)
    f.close()
    i=i+1

i=1
for file in os.listdir(IS_lab_directory):
    print(file)
    parsedfile = parser.from_file(IS_lab_directory + "\\" + file)
    f = open(IS_Save_lab_directory + '\\lab' + str(i) + '.txt', 'w', encoding='UTF-8')
    file_string_with_blank_lines = parsedfile["content"].strip()
    lines = file_string_with_blank_lines.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    file_string_without_empty_lines = ""
    lines_seen = set()
    for line in non_empty_lines:
        if line not in lines_seen: # not a duplicate
            file_string_without_empty_lines += line.strip() + "\n"
            lines_seen.add(line)
    f.write(file_string_without_empty_lines)
    f.close()
    i=i+1


print("---------------------------Artificial Intelligence-------------------------------")
j=1
for file in os.listdir(AI_worksheet_directory):
    print(file)
    parsedfile = parser.from_file(AI_worksheet_directory + "\\" + file)
    f = open(AI_Save_worksheet_directory + '\\worksheet' + str(j) + '.txt', 'w', encoding='UTF-8')
    file_string_with_blank_lines = parsedfile["content"].strip()
    lines = file_string_with_blank_lines.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    file_string_without_empty_lines = ""
    lines_seen = set()
    for line in non_empty_lines:
        if line not in lines_seen: # not a duplicate
            file_string_without_empty_lines += line.strip() + "\n"
            lines_seen.add(line)
    f.write(file_string_without_empty_lines)
    f.close()
    j=j+1

j=1
for file in os.listdir(AI_lecture_directory):
    print(file)
    parsedfile = parser.from_file(AI_lecture_directory + "\\" + file)
    f = open(AI_Save_lecture_directory + '\\slide' + str(j) + '.txt', 'w', encoding='UTF-8')
    file_string_with_blank_lines = parsedfile["content"].strip()
    lines = file_string_with_blank_lines.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    file_string_without_empty_lines = ""
    lines_seen = set()
    for line in non_empty_lines:
        if line not in lines_seen: # not a duplicate
            file_string_without_empty_lines += line.strip() + "\n"
            lines_seen.add(line)
    f.write(file_string_without_empty_lines)
    f.close()
    j=j+1

j=1
for file in os.listdir(AI_lab_directory):
    print(file)
    parsedfile = parser.from_file(AI_lab_directory + "\\" + file)
    f = open(AI_Save_lab_directory + '\\lab' + str(j) + '.txt', 'w', encoding='UTF-8')
    file_string_with_blank_lines = parsedfile["content"].strip()
    lines = file_string_with_blank_lines.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    file_string_without_empty_lines = ""
    lines_seen = set()
    for line in non_empty_lines:
        if line not in lines_seen: # not a duplicate
            file_string_without_empty_lines += line.strip() + "\n"
            lines_seen.add(line)
    f.write(file_string_without_empty_lines)
    f.close()
    j=j+1