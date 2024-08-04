import re

replace01 = [r'\/\/.*\n.*char ', ""]
replace02 = [r'\[+.*\{', "= ("]
replace03 = [r'};', ")"]
replace04 = [r"\/\/.*\n.*\n.*", "all_frame8 = ("]

f = open("raw_cpp.txt", 'r')
content = f.read()
f.close()
content = re.sub(replace01[0], replace01[1], content)
content = re.sub(replace02[0], replace02[1], content)
content = re.sub(replace03[0], replace03[1], content)
content = re.sub(replace04[0], replace04[1], content)
print(content)
fpy = open("FPS_10/hex_arr8.py", 'w')
fpy.write(content)
fpy.close()
