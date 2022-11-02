#!/usr/bin/env python3
def error_section_line(line):
	raise ValueError(f"Supposed section line '{line}' start neither with \"\"\" not with ##")

class Section:
	def __init__(self, name, number = None, level = 1):
		self.level = level
		self.name = name
		self.number = number

	def numstr(self):
		if self.number is None:
			return "?"
		else:
			return str(self.number)

	def __repr__(self):
		prefix = "#" * self.level
		return f"{prefix} {self.numstr()} {self.name}"

	def from_line(line):
		if line.startswith('"""'):
			level = 0
			begin = 3
			end = 3 + line[3:].index('"""')
		elif line.startswith('##'):
			level = 1
			begin = 2
			end = len(line) - 1 #last char is '\n'
		else:
			raise error_section_line(line)

		name = line[begin:end].strip(" ")
		return Section(name, None, level)

def is_new_section(line):
	return (
		line.startswith('"""')
		or line.startswith('##')
	)

class FullSection(list):
	"""list of levels of section: 1.2.3"""
	def __init__(self):
		super().__init__()

	def __repr__(self):
		numbers = '.'.join(map(
			lambda s: s.numstr(),
			self
		))
		return f"{numbers} {self[-1].name}"

	def copy(self):
		return self[:]

	def update(self, section, erase_lower = True):
		level = section.level
		#if the current section levels
		#are not deep enough,
		#extend them
		while level >= len(self):
			self.append(Section("...", 0, len(self)))

		#if this is supposed to trim the info
		#remove all lower levels that are left
		#from previous rounds
		while erase_lower and len(self) > level + 1:
			self.pop()

		if (
			self[level].number is not None
			and section.number is None
		):
			section.number = self[level].number + 1
		self[level] = section

section_templates = {
	0: "\\section{%s}\n",
	1: "\\subsection{%s}\n",
	2: "\\subsubsection{%s}\n",
}
#redefined per LaTeX documentclass
cheat_template = """\\cheat{%s}{%i}{%i}"""
def no_such_level_template(level):
	return KeyError("there's no template for a \
		LaTeX section type of level '%s'" % level)


class Segment:
	def __init__(
		self,
		fullsection,
		lines,
		firstline,
		lastline
	):
		self.section = fullsection
		self.lines = lines
		self.firstline = firstline
		self.lastline = lastline

	def __repr__(self):
		return "".join(
			[repr(self.section) + "\n"]
			+ self.lines
		)

	def read(self, file):
		for line in file:
			if is_new_section(line):
				return line

			self.lines.append(line)
			self.lastline += 1

	def linecount(self):
		return self.lastline - self.firstline

	def latex(self, leave_first_line = False):
		result = ""
		level = len(self.section) - 1
		name = self.section[level].name
		try:
			result += section_templates[level] % name
		except KeyError:
			raise no_such_level_template(level)

		if len(self.lines) > 1:
			result += (cheat_template % (
				name,
				(
					self.firstline + 1
					+ int(leave_first_line)
				),
				self.lastline
			))

		return result

def main(filename = "cheatsheet.py"):
	linecount = 0
	segments = []
	fullsection = FullSection()
	with open(filename, "r") as file:
		#scroll to first section or subsection marking
		segment = Segment(fullsection, [], 0, 0)
		section_line = segment.read(file)
		linecount += segment.linecount() + 1

		while section_line is not None:
			fullsection.update(
				Section.from_line(section_line)
			)
			segment = Segment(
				fullsection.copy(),
				[section_line],
				linecount - 1,
				linecount
			)
			segments.append(segment)

			#read lines for this section
			#until a new [sub]section begins
			section_line = segment.read(file)
			linecount += segment.linecount()

	for segment in segments:
		print(segment.latex(leave_first_line = True))

if __name__ == "__main__":
	main()
