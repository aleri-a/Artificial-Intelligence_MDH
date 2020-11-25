import pandas as pd
import numpy as np 
import sys
import matplotlib.pyplot as plt
NUM_HIDDEN_NEURONS=50
training_percent=0.7
validation_percent=0.1
test_percent=0.2
learning_rate=0.45




def ReadData(nameFile):
    data=pd.read_csv(nameFile)
    x=data.drop("label",axis=1).values   
    y=data['label'].values
    x=x/255
 
    num_data=len(data.index)

    train_size=int(round(training_percent*num_data))
    valid_size=int(round(validation_percent*num_data))
    test_size=int(round(test_percent*num_data))

    x_train=x[:train_size]
    y_train=y[:train_size]

    x_valid=x[train_size:train_size+valid_size]
    y_valid=y[train_size:train_size+valid_size]

    x_test=x[train_size+valid_size:]
    y_test=y[train_size+valid_size:]

    return (x_train,y_train,x_valid,y_valid,x_test,y_test)

class NeuralNetwork:
    def __init__(self,num_columns):   
        self.inputSize=num_columns
        self.outputSize=10
        self.hiddenSize=NUM_HIDDEN_NEURONS

        self.w1=2*np.random.random((self.inputSize,self.hiddenSize))-1 
        self.w2=2*np.random.random((self.hiddenSize,self.outputSize))-1
       

    def Sigmoid(self, z,deriv=False):
        if(deriv==True):
            return z*(1-z)    
        return 1/(1+ np.exp(-z))


    def Train(self,inputs,output):   
        x=inputs.T
        y=output.T

        z1=self.Sigmoid(np.dot(x,self.w1)) #l1
        z2=self.Sigmoid(np.dot(z1,self.w2)) #l2

        error_output=y-z2        
        #backtracking - how much our error did our output layer contributed in our missed output
        output_delta=error_output*self.Sigmoid(z2,True) #deriv sigmoid

        error_hidden=output_delta.dot(self.w2.T)
        hidden_delta=error_hidden*self.Sigmoid(z1,True)
       
        self.w2+=learning_rate*np.dot(z1.T,output_delta) 
        self.w1+=learning_rate*np.dot(x.T,hidden_delta)
        return z2

    def Check(self,inputs, outputs):
        correct=0
        classesTrue=np.zeros(10)
        classesSum=np.zeros(10)
        for i in range(len(inputs)):
            out=self.Forward(inputs[i])
            res=np.argmax(out)
            classesSum[outputs[i]]+=1
            if(res==outputs[i]):
                classesTrue[outputs[i]]+=1
                correct+=1
        print ("Accuracy Of the Network is " , ((correct/len(inputs))*100),"%")
        print ("Accuracy Of each class is ")

        percentageCorrect=[]       
        for i in range(10):
            percentageCorrect.append((classesTrue[i]/classesSum[i])*100)
            print(i,((classesTrue[i]/classesSum[i])*100),"%")
        ShowBarChart((correct/len(inputs)*100),percentageCorrect) 

    def Forward(self,x):
        x=x.T
        z1=self.Sigmoid(np.dot(x,self.w1))
        z2=self.Sigmoid(np.dot(z1,self.w2))
        return z2

def ShowBarChart(netPercent,percentageCorrect):
    labels=[]
    for i in range(len(percentageCorrect)):
        labels.append(str(i))
      #percentageCorrect = [ '%.2f' % elem for elem in my_list ]
    percentageCorrect = list(np.around(np.array(percentageCorrect),2))
    x=np.arange(len(percentageCorrect))
    width = 0.75
    #ypos=np.arange(len(company))
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, percentageCorrect, width, label='percent')
    ax.set_ylabel('Percentage accuracy')

    ax.set_xticks(x)
    ax.set_xticklabels(labels)    
    ax=autolabel(rects1,ax)
    fig.tight_layout()
    
    plt.title('Correctness of the total test data set = %.2f ' % (netPercent), fontsize=10,y=0.05 )
    plt.suptitle("Correctnes of trained ANN",fontsize=15)
    plt.xlabel('Classes')
    
    plt.show()

def autolabel(rects,ax):   
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    return ax

    



def Prepare_output(x):    
    shape=(len(x),10)
    rez=np.zeros(shape,float)
    i=0
    for e in x:
        rez[i][e]=1.0
        i+=1
    return rez


def Progress(count, total, cond=False):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '|' * filled_len + '-' * (bar_len - filled_len)

    if cond == False:
    	sys.stdout.write('[%s] %s%s\r' % (bar, percents, '%'))
    	sys.stdout.flush()

    else:
    	sys.stdout.write('[%s] %s%s' % (bar, percents, '%'))





if __name__=="__main__":
    print("u main")
    x_train,y_train,x_valid,y_valid,x_test,y_test=ReadData("data5.csv") 
    
    y_output = Prepare_output(y_train)
    x_input=[np.reshape(el,(len(x_train[0]),1)) for el in x_train]

    nn=NeuralNetwork(len(x_train[0])) 
    
    it=(len(x_input))

    for i in range(it):
        nn.Train(x_input[i],y_output[i])
        if (i%500)==0:
            Progress(i,it)
    Progress(it, it, cond = True)

    #Validation
    y_output = Prepare_output(y_valid)
    x_input=[np.reshape(el,(len(x_valid[0]),1)) for el in x_valid]
    it=(len(x_input))

    plotProgress=[]
   
    percentage=0
    for i in range(it):
        out=nn.Train(x_input[i],y_output[i])
        realRes=np.argmax(y_output[i])  
        percentage+=out[0][realRes]   
        plotProgress.append(percentage/(i+1))
        if (i%500)==0:
            Progress(i,it)
    Progress(it, it, cond = True)

    axes = plt.gca()
    axes.set_ylim([0.7,1])
    #axes.set_ylim([ymin,ymax])
    plt.plot(plotProgress)
    plt.ylabel('Accurancy')
    plt.xlabel('Number of weights update')
    plt.suptitle('Number hidden neurons = %.2f , learning rate = %.2f ' % (NUM_HIDDEN_NEURONS, learning_rate), fontsize=7)
    plt.title('Changing accuracy in validation set')
    plt.show()





    print ("\n")

    print ("Network is trained. Test is starting ...")

    #test

    test_input=[np.reshape(el,(len(x_test[0]),1)) for el in x_test]
    nn.Check(test_input,y_test)

