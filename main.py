import os
import base64
import zlib
import re
import pathlib
from time import time, sleep
from getpass import getpass
from pystyle import Col, Colors, System, Colorate, Center

dark = Col.dark_gray
light = Colors.StaticMIX((Col.red, Col.red, Col.red))
acc = Colors.StaticMIX((Col.red, Col.red, Col.red, Col.red))
red = Colors.StaticMIX((Col.red, Col.red))
bred = Colors.StaticMIX((Col.red, Col.red))

def p(text):
    return print(stage(text))

def stage(text: str, symbol: str = '...', col1=light, col2=None) -> str:
    if col2 is None:
        col2 = light if symbol == '...' else red
    if symbol in {'...', '!!!'}:
        return f"""     {Col.Symbol(symbol, col1, dark)} {col2}{text}{Col.reset}"""
    else:
        return f""" {Col.Symbol(symbol, col1, dark)} {col2}{text}{Col.reset}"""

import contextlib

text = r"""
██████╗  █████╗ ██╗    ██╗ █████╗     ██████╗ ███████╗ ██████╗ ██████╗ ███████╗██╗   ██╗███████╗ ██████╗ █████╗ ████████╗ ██████╗ ██████╗ 
██╔══██╗██╔══██╗██║    ██║██╔══██╗    ██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝██║   ██║██╔════╝██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
██║  ██║███████║██║ █╗ ██║███████║    ██║  ██║█████╗  ██║   ██║██████╔╝█████╗  ██║   ██║███████╗██║     ███████║   ██║   ██║   ██║██████╔╝
██║  ██║██╔══██║██║███╗██║██╔══██║    ██║  ██║██╔══╝  ██║   ██║██╔══██╗██╔══╝  ██║   ██║╚════██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗
██████╔╝██║  ██║╚███╔███╔╝██║  ██║    ██████╔╝███████╗╚██████╔╝██████╔╝██║     ╚██████╔╝███████║╚██████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
╚═════╝ ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝    ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝      ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝                                                                                                                                       
                                                                                                                                  """

System.Size(150, 47)
os.system("cls && title Hyperion Deobfuscator ^| Made by DAWA TOOL")
print("\n\n")
print(Colorate.Diagonal(Colors.DynamicMIX((red, dark)), Center.XCenter(text)))
print("\n\n")

file = input(stage(f"Faites glisser le fichier que vous souhaitez désobfusquer {dark}-> {Col.reset}", "?", col2=bred)).replace('"', '').replace("'", "")
if file == "":
    file = "in.py"

now = time()
print("\n")
p("Lecture du fichier...")
script = pathlib.Path(file).read_text()

try:
    if "class" not in script:
        p("Le fichier n'est pas obfusquer")
        com = False
        script = script[script.index("b'"):script.rindex("))")]
    else:
        p("Le fichier est obfusquer")
        com, lines = True, []
        for line in script.splitlines():
            if r"=b'" in line:
                p(f"  Une partie de code trouvé dans {acc}" + line[:90].replace(" ", ""))
                a = line[line.find("=b'") + len("=b'"):line.rfind("')")]
                lines.append(a)
        script1 = "".join(lines)
        script = f"b'{script1}'"
    script = zlib.decompress(eval(script)).decode()
except Exception as e:
    p(f"error: {Col.red}{e}{Col.reset}")
    sleep(3)
    exit()

p("Code crypté")

lines0 = script.split("\n")

lines = []
lines.clear()
p("Supression des lignes vides")
lines.extend(line for line in lines0 if len(re.sub(r"\s", "", line)) > 0)
p("Replacing globals")

with contextlib.suppress(Exception):
    os.remove("temp.py")
    os.remove("out.py")
    os.remove("code.py")
    os.remove("vars.py")
    p("Supression des anciens fichiers")

if com:
    p("Supression des crédits")
    lines = lines[13:] 

p("Écriture d'un deuxième fichier : temp.py")
for line in lines:
    with open("temp.py", "a+") as f:
        f.write(line + "\n")

def replace(c, r):
    p(f"replacing {acc}{c[:40]}... {light} with {r[:40]}")
    with open('temp.py', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace(c, r)
    with open('temp.py', 'w') as file:
        file.write(filedata)

def rreplace(c, r):
    p(f"remplacement {acc}{c[27:][:20]}... {light} avec {r[:40]}")
    with open('out.py', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace(c, r)
    with open('out.py', 'w') as file:
        file.write(filedata)

x = 15
llines = 0
p("replacing globals")
p("replacing vars")
for line in lines:
    llines += 1
    if ".join" not in line:
        if len(line) < 150:
            var = line.split("=", 1)[1]
            code = line[line.find(")") + len(")"):line.rfind("="[0])]
            try:
                decrypted = eval(code)
            except:
                decrypted = code
            if "vars" in line:
                code = line[line.find(")") + len(")"):line.rfind("="[0])].replace("[", "").replace("]", "").replace("'", "")
                replace(str(code), "vars")
            decrypted = str(decrypted).replace("[", "").replace("]", "").replace("'", "")
            replace(decrypted, str(var))

    if llines == x:
        break

p("Déclarations décryptées")
with open("temp.py", "r") as f:
    script = f.read().splitlines()
    lines.clear()
    for line in script:
        lines.append(line)

p("Replacing classes with strings")
llines = 0
for line in lines:
    llines += 1
    if ".join" not in line:
        if len(line) > 150:
            var = line.split("=", 1)[1]
            code = line[line.find(")") + len(")"):line.rfind("="[0])].replace("[", "").replace("]", "").replace("'", "")
            decrypted = eval(var)
            decrypted = str(decrypted)
            if "built-in" in decrypted:
                decrypted = decrypted.replace("<built-in function ", "").replace(">", "")
            elif "class" in decrypted:
                decrypted = decrypted.replace("<class '", "").replace("'>", "")
            if "unhexlify" in decrypted:
                decrypted = "binascii.unhexlify"
            replace(str(var), decrypted)
            replace(str(code), decrypted)
    if llines == x:
        break

y = -1

llines = 0
for i in lines:
    llines += 1
    if "from builtins import" in str(i):
        y = llines
        break

if y == -1:
    p("Erreur: Impossible de trouver la ligne de démarrage du script.")
else:
    p(f"Found script start at line {str(y)}")

with open("temp.py", "r") as f:
    script = f.read().splitlines()
    lines.clear()
    for line in script:
        lines.append(line)

p("splitting code into 2 separate files")
p("writing variables to vars.py")
llines = 0
for line in lines:
    llines += 1
    if llines < y and llines > x:
        with open("vars.py", "a+") as f:
            f.write(line + "\n")

p("Ecriture du code : code.py")
llines = 0
for line in lines:
    llines += 1
    if llines >= y:
        with open("code.py", "a+") as f:
            f.write(line + "\n")

p("reading code.py")
with open("code.py", "r") as f:
    script = f.read().splitlines()
    lines.clear()
    for line in script:
        lines.append(line)

llines = 0
p("decrypting second layer")
for line in lines:
    llines += 1
    if "join" in line:
        try:
            code = line[line.find(")") + len(")"):line.rfind("="[0])].replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("'", "")
            var = line.split("=", 1)[1].replace("(", "").replace(")", "")
            decrypted = eval(var)
            replace(str(var), decrypted)
            replace(str(code), decrypted)
        except Exception as e:
            p(f"error: {Col.red}{e}{Col.reset}")

p("reading vars.py")
with open("vars.py", "r") as f:
    script = f.read().splitlines()
    lines.clear()
    for line in script:
        lines.append(line)

p("decrypting second layer vars")
llines = 0
for line in lines:
    llines += 1
    if "join" in line:
        try:
            code = line[line.find(")") + len(")"):line.rfind("="[0])].replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("'", "")
            var = line.split("=", 1)[1].replace("(", "").replace(")", "")
            decrypted = eval(var)
            replace(str(var), decrypted)
            replace(str(code), decrypted)
        except Exception as e:
            p(f"error: {Col.red}{e}{Col.reset}")

p("decrypting final layer")

with open("out.py", "r") as f:
    script = f.read().splitlines()
    lines.clear()
    for line in script:
        lines.append(line)

llines = 0
for line in lines:
    llines += 1
    if "join" in line:
        try:
            code = line[line.find(")") + len(")"):line.rfind("="[0])].replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("'", "")
            var = line.split("=", 1)[1].replace("(", "").replace(")", "")
            decrypted = eval(var)
            replace(str(var), decrypted)
            replace(str(code), decrypted)
        except Exception as e:
            p(f"error: {Col.red}{e}{Col.reset}")

print(Colorate.Vertical(Colors.DynamicMIX((red, dark)), Center.XCenter(f"\n\nsuccessfully decrypted file in {round(time() - now, 2)}s !")))
p("removing temp files")
with contextlib.suppress(Exception):
    os.remove("temp.py")
    os.remove("vars.py")
    os.remove("code.py")
p(f"{Col.green}successfully deobfuscated file {dark}->{Col.green} out.py{Col.reset} !")
getpass(stage("press ENTER to exit", "!", col2=bred))
exit()
