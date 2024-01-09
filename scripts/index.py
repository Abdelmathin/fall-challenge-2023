import os

content = ""

imports = []

for basename in os.listdir("../sources/Java"):
	filename = "../sources/Java/" + basename
	if (filename.endswith(".java")):
		for line in open(filename, "r"):
			_line = line.strip()
			if not _line:
				continue
			if (_line.startswith("package ")):
				continue
			if (_line.startswith("//")):
				continue
			if line.startswith("import "):
				line = line.strip()
				if not (line in imports):
					imports.append(line.strip())
				continue
			content += line
ims = ""
for _import in imports:
	if not _import.startswith("import java."):
		continue
	ims += _import + "\n"

content = ims + content

content = content.replace("public class", "class")
content = content.replace("public enum", "enum")
content = content.replace("public interface", "interface")
content = content.replace("public abstract", "abstract")
content = content.replace("public @interface", "@interface")

with open("../Answer/Answer.java", "w") as fp:
	fp.write(content)
