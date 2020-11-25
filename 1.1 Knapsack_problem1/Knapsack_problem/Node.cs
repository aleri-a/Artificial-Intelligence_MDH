using System;
using System.Collections.Generic;
using System.Text;

namespace Knapsack_problem
{

    
   public  class Node
    {
       public Node parent;
       public  Item info;
       public  int depth=0; //The number of nodes on the path from the root (initial state) to this node
       public  int pathCost=0; //The path-costof the path from the initial state to the node. 
        public int benefit = 0;

        public Node(Node parent, Item info, int dept, int pathCost, int benefit)
        {
            this.depth += dept;
            this.info = info;
            this.parent = parent;
            this.pathCost += pathCost;
            this.benefit += benefit;
        }

        public Node()
        {
            this.benefit = 0;
            this.depth = 0;
            this.info = new Item();
            this.parent = null;
            this.pathCost = 0;
        }
    }
}
