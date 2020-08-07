#########################################################################
#       (C) 2020-2021 Petroleum Engineering Modelling Laboratory,       #
#       Federal University of Paraíba, João Pessoa, BR.                 #
#                                                                       #
# This code is released under the terms of the BSD license, and thus    #
# free for commercial and research use. Feel free to use the code into  #
# your own project with a PROPER REFERENCE.                             #
#                                                                       #
# APyCE Project                                                         #
# Author: Mateus Tosta                                                  #
# Email: mateustosta@outlook.com.br                                     #
#########################################################################

from collections import OrderedDict as OD
import string
import re

try:
	from vtk import *
	import numpy as np
except ImportError:
	print("No VTK/NumPy module loaded.")

########################################
#  Main class of APyCE                 #
#                                      #
#  Input: CMG Builder/Eclipse File 	   #
#  Output: VTK file and GRDECL file    #
########################################

class Model:
	def __init__(self, filename=''):
		"""
		Supported Keywords:
		SPECGRID - NX, NY, NZ
		COORDS, ZCORN, ACTNUM, and PORO

		References: http://www.mj-oystein.no/index_htm_files/ResSimNotes.pdf

		Author: Mateus Tosta (mateustosta@outlook.com.br)
		Date: Jul. 2020
		"""
		self.fname = filename
		self.FileOpenException(self.fname)

		self.NX, self.NY, self.NZ, self.COORDS, self.ZCORN, self.ACTNUM, self.PORO = self.ReadFile(self.fname)

		### A partir daqui eu não entendo
		self.vtkUnstructuredGrid = vtkUnstructuredGrid()

		self.xcoords = self.COORDS[0::3]
		self.xcoords = list(OD.fromkeys(self.xcoords))
		self.ycoords = self.COORDS[1::3]
		self.ycoords = list(OD.fromkeys(self.ycoords))

		self.vtkUnstructuredGrid = self.CreateVTKCells(self.vtkUnstructuredGrid, self.NX, self.NY, self.NZ)
		self.vtkUnstructuredGrid.SetPoints(self.CreateVTKPoints(self.xcoords, self.ycoords, self.ZCORN))

		self.vtkUnstructuredGrid.GetCellData().AddArray(self.CreateVTKArray('ACTNUM', self.ACTNUM))
		self.vtkUnstructuredGrid.GetCellData().AddArray(self.CreateVTKArray('PORO', self.PORO))

		self.WriteVTK(self.vtkUnstructuredGrid, self.fname)

	def FileOpenException(self, filename):
		try:
			file = open(filename, 'r')
			file.close()
		except IOError:
			print("Oops! Can't find/open the file. Try again...")
			exit()

	def ReadFile(self, filename):
		"""
		Read input file

		Author: Mateus Tosta (mateustosta@outlook.com.br)
		Date: Jul. 2020
		"""
		print("\n[Input] Reading CMG Builder file \"" + filename + "\" ....\n")

		file = open(filename, 'r')

		# Keywords
		specgrid = list()
		coords = list()
		zcorn = list()
		actnum = list()
		poro = list()
		NX, NY, NZ = None, None, None
		dim = None

		keywords = ["SPECGRID", "COORD", "ZCORN", "ACTNUM", "PORO"]

		for line in file:
			if line.startswith("COORDSYS"):
				continue
			elif line.startswith("SPECGRID"):
				print("Keyword SPECGRID found")
				line = file.readline()
				specgrid = np.array(re.findall(r'\d+',str(line)), dtype=int)
				NX, NY, NZ = specgrid[0], specgrid[1], specgrid[2]
				dim = NX * NY * NZ

				print("\tGrid Dimension: {} x {} x {}".format(NX,NY,NZ))
				print("\tNumOfGridCells:",dim)
				print("....Done!\n")
			elif line.startswith("COORD"):
				print("Keyword COORD found")
				while True:
					line = file.readline()
					if not '/' in line:
						values = self.ExpandsScalars(line)
						coords.extend(values)
					if '/' in line:
						coords = list(map(float, coords))
						break
				print("....Done!\n")
			elif line.startswith("ZCORN"):
				print("Keyword ZCORN found")
				while True:
					line = file.readline()
					if not '/' in line:
						values = self.ExpandsScalars(line)
						zcorn.extend(values)
					if '/' in line:
						zcorn = list(map(float, zcorn))
						break
				print("....Done!\n")
			elif line.startswith("ACTNUM"):
				print("Keyword ACTNUM found")
				while True:
					line = file.readline()
					if not '/' in line:
						values = self.ExpandsScalars(line)
						actnum.extend(values)
					if '/' in line:
						actnum = list(map(int, actnum))
						break
				print("....Done!\n")
			elif line.startswith("PORO"):
				print("Keyword PORO found")
				while True:
					line = file.readline()
					if not '/' in line:
						values = self.ExpandsScalars(line)
						poro.extend(values)
					if '/' in line:
						poro = list(map(float, poro))
						break
				print("....Done!\n")
			elif line.startswith("INCLUDE"):
				print("Keyword INCLUDE found")
				line = file.readline()
				includeFilename = "./Data/" + line.split("\'")[1]
				self.FileOpenException(includeFilename)
				includeFile = open(includeFilename, 'r')
				line_includeFile = includeFile.readline()
				for key in keywords:
					if line_includeFile.startswith("COORDSYS"):
						continue
					if line_includeFile.startswith(key):
						print("Keyword "+key+" found")
						if key == "SPECGRID":
							line_includeFile = includeFile.readline()
							specgrid = np.array(re.findall(r'\d+', str(line_includeFile)), dtype=int)
							NX, NY, NZ = specgrid[0], specgrid[1], specgrid[2]
							dim = NX * NY * NZ

							print("\tGrid Dimension: {} x {} x {}".format(NX,NY,NZ))
							print("\tNumOfGridCells:",dim)
							print("....Done!\n")
							break
						elif key == "COORD":
							while True:
								line_includeFile = includeFile.readline()
								if not '/' in line_includeFile:
									values = self.ExpandsScalars(line_includeFile)
									coords.extend(values)
								if '/' in line_includeFile:
									coords = list(map(float ,coords))
									break
							print("....Done!\n")
							break
						elif key == "ZCORN":
							while True:
								line_includeFile = includeFile.readline()
								if not '/' in line_includeFile:
									values = self.ExpandsScalars(line_includeFile)
									zcorn.extend(values)
								if '/' in line_includeFile:
									zcorn = list(map(float, zcorn))
									break
							print("....Done!\n")
							break
						elif key == "ACTNUM":
							while True:
								line_includeFile = includeFile.readline()
								if not '/' in line_includeFile:
									values = self.ExpandsScalars(line_includeFile)
									actnum.extend(values)
								if '/' in line_includeFile:
									actnum = list(map(int, actnum))
									break
							print("....Done!\n")
							break
						elif key == "PORO":
							while True:
								line_includeFile = includeFile.readline()
								if not '/' in line_includeFile:
									values = self.ExpandsScalars(line_includeFile)
									poro.extend(values)
								if '/' in line_includeFile:
									poro = list(map(float, poro))
									break
							print("....Done!\n")
							break
				includeFile.close()
		file.close()
		return NX, NY, NZ, coords, zcorn, actnum, poro

	def ExpandsScalars(self, line):
		values = list()
		for scalar in line.split():
			if not "*" in scalar:
				values.append(scalar)
			else:
				tmp = scalar.split("*")
				tmp = [tmp[1]] * int(tmp[0])
				values.extend(tmp)
		return values


	def CreateVTKCells(self, vtkUnstructuredGrid, NX, NY, NZ):
		cellZeroPattern = [0, 1, 2*NX, 2*NX+1, 4*NY*NX, 4*NY*NX+1, 4*NY*NX+2*NX, 4*NY*NX+2*NX+1]

		for k in range(NZ):
			for j in range(NY):
				for i in range(NX):
					cell = vtkHexahedron()
					pattern = [x+(2*i)+(4*j*NX)+(8*k*NX*NY) for x in cellZeroPattern]

					cell.GetPointIds().SetId(0, pattern[0])
					cell.GetPointIds().SetId(1, pattern[1])
					cell.GetPointIds().SetId(2, pattern[3])
					cell.GetPointIds().SetId(3, pattern[2])
					cell.GetPointIds().SetId(4, pattern[4])
					cell.GetPointIds().SetId(5, pattern[5])
					cell.GetPointIds().SetId(6, pattern[7])
					cell.GetPointIds().SetId(7, pattern[6])

					vtkUnstructuredGrid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())
		return vtkUnstructuredGrid

	def CreateVTKPoints(self, x, y, z):
		i = 0
		j = 0
		pts = vtkPoints()
		repeatY = False
		for k in range(0,len(z)-1,2):
			p1 = [x[i], y[j], z[k]]
			p2 = [x[i+1], y[j], z[k+1]]
			pts.InsertPoint(k, p1)
			pts.InsertPoint(k+1, p2)
			i = i + 1
			if i > len(x) - 2:
				i = 0
				if not repeatY:
					if j < len(y) - 1:
						j = j + 1
						repeatY = True
						if j == len(y) - 1:
							repeatY = False
					elif j == len(y) - 1:
						j = 0
				else:
					repeatY = False
		return pts

	def CreateVTKArray(self, keyword, values):
		fa = vtkFloatArray()
		fa.SetName(keyword)
		fa.SetNumberOfComponents(1)
		for i in values:
			fa.InsertNextTuple1(i)
		return fa

	def WriteVTK(self, vtkUnstructuredGrid, filename):
	    filename = filename.split("/")[2]
	    filename = filename.split(".")[0]
	    legacyWriter = vtkUnstructuredGridWriter()
	    legacyWriter.SetFileName('./Data/' + filename + '.vtk')
	    legacyWriter.SetInputData(vtkUnstructuredGrid)
	    legacyWriter.Write()

Model('./Data/MAC7A-TM02.txt')