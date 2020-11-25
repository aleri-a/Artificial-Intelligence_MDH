#pragma once
#include <string>
#include <fstream>
#include <stdio.h>
using namespace std;
class ReadingFile
{
public:
	void ReadSudoku(string name, int numSud, char sudoku[9][9])
	{
		ifstream file(name);
		//char sudoku[9][9];
		if (file.is_open())
		{
			string line;
			while (line != "SUDOKU " + to_string(numSud) && !file.eof())
				getline(file, line);

			int i = 0;
			while (i < 9)
			{
				int j = 0;
				getline(file, line);
				while (j < 9 && j < line.length())
				{
					sudoku[i][j] = line[j];
					j++;
				}
				i++;
			}
			
		}
		file.close();
		

	}


};

