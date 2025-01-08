import random
import math
import pandas as pd

DATFRAME_COLUMN_A = ["U", "P", "X", "Y", "Z", "W", "V", 'ITER']
DATFRAME_COLUMN_B = ["U", "P", "X", "Y", "Z", "W", 'ITER']

"""
substructure A
       *(U)
       |
      *(P)
   /   |
 *(W)  *(X)
   |   |
 *(V)  *(Y)
       |
       *(Z)
"""
class subgraph_A:
  def __init__(self, status):
    self.P = None
    self.X = None
    self.Y = None
    self.Z = None
    self.W = None
    self.V = None
    self.set_status(status)
  
  def set_status(self, status):
    self.P = status[0]
    self.X = status[1]
    self.Y = status[2]
    self.Z = status[3]
    self.W = status[4]
    self.V = status[5]

"""
substructure B
       *(U)
       |
      *(P)
    /  |
  *(W) *(X)
    \  |
      *(Y)
       |
       *(Z)
"""
class subgraph_B:
  def __init__(self, status):
    self.P = None
    self.X = None
    self.Y = None
    self.Z = None
    self.W = None
    self.set_status(status)
  
  def set_status(self, status):
    self.P = status[0]
    self.X = status[1]
    self.Y = status[2]
    self.Z = status[3]
    self.W = status[4]



"""
This class is used to decide whether the devices are broken by providing the probability
"""
class well_decider:
  def __init__(self, broken_prob):
    self.values = [False, True]
    self.weights = [100 - broken_prob, broken_prob]  
  """
  return type -> list
  this method will return a bool list which represents the status of corresponding devices
  """
  def decide_broken(self, nums):
    return random.choices(self.values, self.weights, k = nums)


"""
the omega function
---------------------
False: not broken
True:  broken
---------------------
truth table:
p -> u     v     |  omega(p,u,v)
---------------------
0    0     0     |   0
0    0     1     |   1
0    1     0     |   1
0    1     1     |   1
1   ...   ...    |   X(randon return 0/1)
"""
def check_device(p,u,v):
  if(p == False):
    return u or v
  else:
    """
    Probability of Correctly Diagnosing Faulty Nodes: 50%
    """
    #values = [False, True]
    #weight = [50, 50]
    #return random.choices(values, weight, k = 1)[0]
    """
    Probability of Correctly Diagnosing Faulty Nodes: fp%
    """
    fp = 50
    values = [0, 1]
    weight = [100-fp, fp]
    if(random.choices(values, weight, k = 1)[0] == 0):
        return u or v
    else:
        return not(u or v)

class DirectionalDiagnosisStructure(well_decider):
  def __init__(self, iter, broken_prob):
    well_decider.__init__(self, broken_prob)
    self.iter = iter
    #  status of root node 
    self.U = self.decide_broken(1)[0]
    self.cluster_A = list()
    self.cluster_B = list()
    self.df_A = pd.DataFrame(columns=DATFRAME_COLUMN_A)
    self.df_B = pd.DataFrame(columns=DATFRAME_COLUMN_B)
    self.a = 0
    self.b = 0
    self.result = -1
    self.test_types = -1
  
  def add_subgraph_A(self, nums):
    self.a = nums
    for idx in range(nums):
      sub = subgraph_A(self.decide_broken(6))
      self.df_A.loc[len(self.df_A.index)] = [self.U, sub.P, sub.X, sub.Y, sub.Z, sub.W, sub.V, self.iter]
      self.cluster_A.append(sub)

  def add_subgraph_B(self, nums):
    self.b = nums
    for idx in range(nums):
      sub = subgraph_B(self.decide_broken(5))
      self.df_B.loc[len(self.df_B.index)] = [self.U, sub.P, sub.X, sub.Y, sub.Z, sub.W, self.iter]
      self.cluster_B.append(sub)

  #def printf_data(self):
    #print(self.df_A)
    #print(self.df_B)
  # Local diagnosis algorithm for mixed structure 
  
  def LDAM(self):
    a = self.a
    b = self.b
    ab= 0
    if(a > 0):
      for cluster in self.cluster_A:
        check_result = [check_device(cluster.P, self.U, cluster.X), check_device(cluster.Y, cluster.X, cluster.Z), check_device(cluster.W, cluster.P, cluster.V)]
        if check_result == [0, 0, 0]:
          ab += 1
        elif check_result == [1, 0, 0]:
          ab += -1
    
    if(b > 0):
      for cluster in self.cluster_B:
        check_result = [check_device(cluster.P, self.U, cluster.X), check_device(cluster.Y, cluster.X, cluster.Z), check_device(cluster.W, cluster.P, cluster.Y)]
        if check_result == [0, 0, 0]:
          ab += 1
        elif check_result == [1, 0, 0]:
          ab += -1

          
    # 1: TN, 2: FN, 3: FP, 4:TP 
    if ab >= 0:
      self.result = 0
      if self.U == False:
        self.test_types = 1
      else:
        self.test_types = 2 
    else:
      self.result = 1
      if self.U == False:
        self.test_types = 3
      else:
        self.test_types = 4