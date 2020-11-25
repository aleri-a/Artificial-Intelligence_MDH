using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using System.Text.RegularExpressions;
namespace Knapsack_problem
{
    static public class IOFiles
    {


        public static (int, List<Item>) ReadFile(string inputName)
        {
            List<Item> items = new List<Item>();
            int bagWeight = 0;

            if (inputName.Length < 4 || inputName.Substring(inputName.Length - 4) != ".txt")
                inputName += ".txt";
            String path = Environment.CurrentDirectory + @"\" + inputName;
            Console.WriteLine(path);
            if (File.Exists(path))
            {
                foreach (var line in File.ReadLines(path, Encoding.UTF8))
                {
                    if (!string.IsNullOrEmpty(line))
                    {
                        if (line.Contains("MAXIMUM WEIGHT: "))
                            bagWeight = Int32.Parse(Regex.Match(line, @"\d+").Value); //da nadjem samo brojeve u toj liniji 
                        if (char.IsDigit(line[0]))
                        {
                            string[] valStr = line.Split(' ');
                            items.Add(new Item(Int32.Parse(valStr[0]), Int32.Parse(valStr[1]), Int32.Parse(valStr[2])));
                        }
                    }
                }


            }
            else
                Console.WriteLine("Input file name doesn't exist");
            
            return (bagWeight,items);
        }




        public static bool WriteFile(String outputName, List<String> txt)
        {

            if (outputName.Length < 4 || outputName.Substring(outputName.Length - 4) != ".txt")
                outputName += ".txt";


            using (StreamWriter writetext = new StreamWriter(outputName))
            {
                foreach (string line in txt)
                    writetext.WriteLine(line + "\n");
                return true;
            }

            
        }
    }
}
