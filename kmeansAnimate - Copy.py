import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["animation.convert_path"] = "C:\Program Files\ImageMagick-7.0.9-Q16\magick.exe" 
from matplotlib import animation
from matplotlib.animation import PillowWriter
import random as rnd, numpy as np
import seaborn as sns;sns.set();
np.set_printoptions(suppress=True)




class kmeans_classifier:
    def __init__(self,df,k=None):
        self.df = df
        self.k, self.length = k, len(df)
        self.X = df.values
        self.dimensions = len(self.X[0])
        self.centroids = np.copy(self.X[np.random.choice(self.X.shape[0], \
                                            self.k, replace=False), :])
        
        self.distances = np.zeros((2,self.length))
   
        self.objective_funtion = []
        self.fig = plt.figure()
        self.colors = []
        self.offsets = []
    def get_ssd(self,pi,p):
        ssd = 0
        for i in range(self.dimensions):
            ssd += (pi[i]- p[i])**2
        return ssd
    
    def get_distance(self):
        self.distances[0].fill(9999999999)
        self.distances[1].fill(0)
        obj = 0
        for i in range(self.k):
            for j in range(self.length):
                ssd = self.get_ssd(self.X[j],self.centroids[i])
                
                if self.distances[0][j]>ssd:
                    self.distances[0][j] = ssd
                    self.distances[1][j] = i
                    
        self.objective_funtion.append(np.sum(self.distances[0]))
        return self.distances

        

    def get_centroids(self):
        cen_c = np.zeros(self.k,int)
        self.centroids.fill(0)
        for i in range(self.length):
            for j in range(self.dimensions):
                self.centroids[int(self.distances[1][i])][j] += self.X[i][j]
            cen_c[int(self.distances[1][i])] += 1
        
        for i in range(self.k):
            for j in range(self.dimensions):
                self.centroids[i][j] /= cen_c[i]
        return self.centroids
    
    def plotObjectiveFunction(self):
        index = [i for i in range(len(self.objective_funtion))]
        sns.scatterplot(index,self.objective_funtion,s = 50,edgecolor='k',**{'color':'r'})
        sns.lineplot(index,self.objective_funtion)
        plt.show()
        
    def clustering(self):
        self.get_distance()
        
        limit = 0
        while(limit!=50):
            limit += 1
            self.colors.append(np.copy(self.distances[1]))
            self.offsets.append(np.copy(self.centroids))
            self.get_centroids() 
            self.get_distance()
            if self.objective_funtion[-1]==self.objective_funtion[-2]:
                break
    def setup_plot(self):
        self.scat = plt.scatter(x=self.X[:,0],y=self.X[:,1],s=50,\
                c=self.colors[0],cmap='plasma',edgecolor='k')
        self.scat2 = plt.scatter(x=self.offsets[0][:,0],y=self.offsets[0][:,1],\
                c='w',s=70,marker='X',edgecolor='k')
        
        return self.scat2,self.scat
    
    def update(self, i):
        self.scat.set_array(self.colors[i])
        self.scat2.set_offsets(self.offsets[i])
        
        return self.scat,self.scat2

def main():
    df = pd.read_csv("Iris.csv")
    df = df[df.columns[:2]]
    
    clf = kmeans_classifier(df,3)
    clf.clustering()
    ani = animation.FuncAnimation(clf.fig,clf.update,frames=range(len(clf.colors)),
                                  init_func=clf.setup_plot,interval=500,repeat=True,blit=True)

    #plt.show()
    ani.save("test.gif",writer="imagemagick", extra_args="convert")
   
   
    
    
main()
print('end')
