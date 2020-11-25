using System;
using System.Collections.Generic;
using System.Text;

namespace Knapsack_problem
{
    public class Bag
    {
        List<Item> items;
        int maxWeight;

        public Bag(int maxW, List<Item> it)
        {
            items = new List<Item>(it);
            this.maxWeight = maxW;
           // items = IOFiles.ReadFile(nameInputFile);
        }

        public Queue<Item> MakeOrderedQueue()
        {
            SortedList<int, Item> queue = new SortedList<int, Item>();
            foreach (var v in this.items)
                queue.Add(v.EvaluationValue(), v);
            Queue<Item> qu = new Queue<Item>();
            foreach (var v in queue)
                qu.Enqueue(v.Value);                        
            return qu;
        }

        //All the nodes at depth d are expanded before the nodes in depth d+1
        public Node BFS()
        {
            SortedList<int, Node> result = new SortedList<int, Node>();
            //result.Add(0, new Node());
            Queue<Node> queueMain = new Queue<Node>();
            foreach (Item i in items)
            {
                Node n = new Node(null, i, 1, i.weight,i.benefit);
                queueMain.Enqueue(n);
                
                
            }

            while(queueMain.Count>0)
            {
                Node curr = new Node();
                curr = queueMain.Dequeue();

                if (  curr.pathCost <= maxWeight && ( result.Count==0 ||curr.benefit>result.Values[result.Count-1].benefit ) )             
                    result.Add(curr.benefit, curr);

                foreach(Item it in items)
                {
                    if(it.id>curr.info.id)
                    {
                        int newPathCost = curr.pathCost + it.weight;
                        if (newPathCost<=maxWeight)
                        {
                            Node newN = new Node(curr, it, curr.depth + 1, newPathCost,curr.benefit+it.benefit);
                            queueMain.Enqueue(newN);
                        }
                    }
                }
            }
            return result.Values[result.Count-1];
           
        }


        public Node DFS()
        {
            SortedList<int, Node> result = new SortedList<int, Node>();
            //result.Add(0, new Node());
            Stack<Node> queueMain = new Stack<Node>();
            foreach (Item i in items)
            {
                Node n = new Node(null, i, 1, i.weight, i.benefit);
                queueMain.Push(n);
            }

            while (queueMain.Count > 0)
            {
                Node curr = new Node();
                curr = queueMain.Pop();

                if (curr.pathCost <= maxWeight && (result.Count == 0 || curr.benefit > result.Values[result.Count - 1].benefit))
                    result.Add(curr.benefit, curr);

                foreach (Item it in items)
                {
                    if (it.id > curr.info.id)
                    {
                        int newPathCost = curr.pathCost + it.weight;
                        if (newPathCost <= maxWeight)
                        {
                            Node newN = new Node(curr, it, curr.depth + 1, newPathCost, curr.benefit + it.benefit);
                            queueMain.Push(newN);
                        }
                    }
                }
            }
            return result.Values[result.Count - 1];

        }



        public void Check()
        {
            SortedList<int, int> queue = new SortedList<int, int>();
            foreach (Item i in items)
            {               
                    queue.Add(i.EvaluationValue(), i.id);
            }
        }

        //DFS 
        //BFS
    }
}
