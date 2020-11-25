using System;
using System.Diagnostics;

namespace Knapsack_problem
{
   public class Program
    {
       
       static void  Main(string[] args)
        {
           
            var res=IOFiles.ReadFile("input");
            Bag bag = new Bag(res.Item1, res.Item2);

            var timer = new Stopwatch();

            timer.Start();
            Node n= bag.BFS();
            timer.Stop();
            Console.WriteLine("BFS: " + timer.Elapsed.TotalSeconds.ToString("#,##0.0000000 'seconds'"));
           

            timer.Start();
            Node nDfs = bag.DFS();
            timer.Stop();
            Console.WriteLine("BFS: " + timer.Elapsed.TotalSeconds.ToString("#,##0.000000 'milliseconds'"));
            
        }



        public void PrintResult(Node nDfs)
        {

            while (nDfs.parent != null)
            {
                Console.WriteLine(nDfs.info.id + " (" + nDfs.info.benefit + ", " + nDfs.info.weight + ") ");
                nDfs = nDfs.parent;
            }
            Console.WriteLine(nDfs.info.id + " (" + nDfs.info.benefit + ", " + nDfs.info.weight + ") ");

        }
    }
}
