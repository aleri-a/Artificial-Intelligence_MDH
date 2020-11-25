// Makao-Backtracking.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "ReadingFile.h"
#include <time.h>
#include <stdio.h>
#include <chrono>
using namespace std;
using namespace chrono;


void PrintSudoku(char sudoku[9][9]);
int CheckSquer(char sudoku[9][9], int  line, int  column, char  num);
bool FindEmpty(char sudoku[9][9], int place[2]);
bool ContainsNum(char matrica[9][9], char el);
bool PotentialNumber(char sudoku[9][9], int line, int column, int numb);
bool Backtrack(char sudoku[9][9]);

int main()
{
	cout << "Hello World!\n";
	ReadingFile readFile;
	char sudoku[9][9];
	double sumTime = 0;
	for (int i = 1; i <= 10; i++)
	{
		
		cout << "\nSUDOKU: " << i<<"\n";

		readFile.ReadSudoku("input.txt", 10, sudoku);
		
		//PrintSudoku(sudoku);
		steady_clock::time_point begin = steady_clock::now();
		Backtrack(sudoku);
		steady_clock::time_point end = steady_clock::now();
		double dif = duration_cast<microseconds>(end - begin).count();
		sumTime += dif;
		PrintSudoku(sudoku);
		cout << "Time difference = " << dif<< "microsecunds" << endl;
	}
	cout << "Sum time: " << sumTime << " microseconds\n";
	cout << "Sum time: " << sumTime/1000000 << " seconds";

	
}


void PrintSudoku(char sudoku [9][9])
{
	for (int i = 0; i < 9; i++) {
		string pom = "";
		if (i % 3 == 0)
			cout << "_________________________________\n";
		for (int j = 0; j < 9; j++) {
			if (j % 3 == 0)
				pom += " |";
			pom+=sudoku[i][j];
			pom += " ";
		}
		cout << pom;
		cout << '\n';
		
		
	}
}



bool FindEmpty(char sudoku[9][9], int place[2])
{
	for (int i = 0; i < 9; i++)
	{
		for (int j = 0; j < 9; j++) {
			if (sudoku[i][j] == '0') {
				place[0] = i;
				place[1] = j;
				return true;
			}
		}
	}
	return false;

}

bool ContainsNum(char matrica[9][9], char el) {
	for(int i=0;i<9;i++)
		for (int j = 0; j < 9; j++) {
			if (matrica[i][j] == el)
				return true;
		}
	return false;
}

bool PotentialNumber(char sudoku[9][9], int line, int column, int numb) {
	int i = '0' + numb;
	
	for (int jj = 0; jj < 9; jj++)		
		if (int(sudoku[line][jj]) == i)
			return false;

	for (int jj = 0; jj < 9; jj++) 
		if (int(sudoku[jj][column]) == i)
			return false;

	int sq = CheckSquer(sudoku, line, column, i);
	if (sq == -1)
		return false;

	return true;
}
//static_cast<char>(numb)

int CheckSquer(char sudoku[9][9],int  line,int  column,char  num) {
	int fiLine = (line / 3) * 3;
	int fiColumn = (column / 3) * 3;
	int counterLine = 0;
	while(counterLine < 3){
		int counterColumn = 0;
		while (counterColumn < 3)
		{
			if (num == sudoku[fiLine + counterLine][fiColumn + counterColumn]) {
				return -1;
			}
			counterColumn += 1;
		}
		counterLine += 1;
	}
	return 1;
}

bool Backtrack(char sudoku[9][9])
{
	int empt[2] = { -1,-1 };
	bool found = FindEmpty(sudoku, empt);
	if (!found) 
		return true;
	int i = empt[0];
	int j = empt[1];

	for (int numb = 1; numb < 10; numb++) {
		bool existNo = PotentialNumber(sudoku, i, j, numb); //ako postoji taj br vratice false 
		//tj ako mozes da koristis taj br vraca true 
		if (existNo) {
			sudoku[i][j] = '0'+numb;
			if (Backtrack(sudoku))
				return true;
			else
				sudoku[i][j] = '0';
			
		}
	}
	return false;

}


