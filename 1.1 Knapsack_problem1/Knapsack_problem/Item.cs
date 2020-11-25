using System;
using System.Collections.Generic;
using System.Text;

namespace Knapsack_problem
{
    public class Item
    {
       public int id;
       public  int weight;
       public  int benefit;

        public Item(int id, int benefit, int weight)
        {
            this.id = id;
            this.benefit = benefit;
            this.weight = weight;
        }
        public Item()
        {
            this.benefit = 0;
            this.id = -1;
            this.weight = 0;
        }


        public int EvaluationValue()
        {
            return benefit - weight;
        }

    }
}
