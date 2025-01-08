from structure import DirectionalDiagnosisStructure, check_device
import argparse
import pandas as pd
import os

def main():
  """
  sample : run main.py -a 2 -b 2 -p 20 -i 500
  # substructure A: 2
  # substructure B: 2
  broken probability: 20 %
  """
  parser = argparse.ArgumentParser()
  parser.add_argument('-a', type = int, help="# of substructure A")
  parser.add_argument('-b', type = int, help="# of substructure B")
  parser.add_argument('-p', type = float, help="broken probability")
  parser.add_argument('-i', type = int, help="iteration times")
  args = parser.parse_args()
  total_iteration = args.i
  sturcture_a = list() 
  sturcture_b = list() 
  results = list()
  state_U = list()
  types = list()
   
  for iter in range(total_iteration):
    graph = DirectionalDiagnosisStructure(iter, args.p)
    graph.add_subgraph_A(args.a)
    graph.add_subgraph_B(args.b)
    graph.LDAM()
    sturcture_a.append(graph.df_A)
    sturcture_b.append(graph.df_B)
    state_U.append(graph.U)
    results.append(graph.result)
    types.append(graph.test_types)
  
  df_a = pd.concat(sturcture_a)
  df_b = pd.concat(sturcture_b)
  dir_name = 'a{}_b{}_p{}_i{}'.format(args.a, args.b, args.p, args.i)
  print(dir_name)
  os.mkdir(dir_name)
  filename_a = os.path.join(dir_name, "a.csv")
  filename_b = os.path.join(dir_name, "b.csv")
  df_a.to_csv(filename_a)
  df_b.to_csv(filename_b)

  dict = {'U': state_U, 'result': results, 'iter':range(total_iteration), 'type': types}
  df_result = pd.DataFrame(dict)
  filename_result = os.path.join(dir_name, "result.csv")
  df_result.to_csv(filename_result)

if __name__ == '__main__':
  main()
