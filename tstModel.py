from model.model import Model

mymodel = Model()
mymodel.buildGraph("France", 2015)
score,path=mymodel.getPercorso(5)
print(score)
print(path)