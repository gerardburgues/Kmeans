
import numpy as np
import utils
import random


class KMeans:

    def __init__(self, X, K=1, options=None):
      
        self.num_iter = 0
        self.K = K
        self._init_X(X)
        self._init_options(options) 





    def _init_X(self, X):

        np.dtype(float)
        rows =len(X)
        colum= len(X[-1])

        N = rows * colum
        
        if X.ndim > 2:
            
            self.X = np.reshape(X,(N ,X.shape[-1]))


    def _init_options(self, options=None):
       
        if options == None:
            options = {}
        if not 'km_init' in options:
            options['km_init'] = 'first'
        if not 'verbose' in options:
            options['verbose'] = False
        if not 'tolerance' in options:
            options['tolerance'] = 0
        if not 'max_iter' in options:
            options['max_iter'] = np.inf
        if not 'fitting' in options:
            options['fitting'] = 'WCD'  #within class distance.

    
        self.options = options


    def _init_centroids(self):

        if self.options['km_init'].lower() == 'first':

           u,idx=np.unique(self.X,axis=0,return_index=True)

           self.centroids= self.X[np.sort(idx)]
           self.centroids= self.centroids[:self.K]
           self.centroids = self.centroids.astype(float)


           u,idx=np.unique(self.X,axis=0,return_index=True)
           self.old_centroids= self.X[np.sort(idx)]
           self.old_centroids= self.old_centroids[:self.K]
           self.old_centroids = self.centroids.astype(float)



        else:
            self.centroids = np.random.rand(self.K, self.X.shape[1])
            self.old_centroids =np.random.rand(self.K, self.X.shape[1])


    def get_labels(self):

        dist = distance(self.X, self.centroids)

        self.labels = np.argmin(dist,axis=1)



    def get_centroids(self):


        np.copyto(self.old_centroids, self.centroids)
        x= np.array([])
        i=0
        while i<self.K:

            result = np.where(self.labels == i)

            echo = self.X[result]
            suma = np.sum(self.X[result],axis=0)
            suma = suma/echo.shape[0]
            x = np.append(x,suma, axis=0 )

            i=i+1

        self.centroids = x.reshape(-1,self.X.shape[1])


    

    def converges(self):
        """
        Checks if there is a difference between current and old centroids
        """

        equal = np.array_equal(self.centroids, self.old_centroids)

        return equal

    def fit(self):


        self._init_centroids()
        i=0
        continua =True
        while continua == True:
            self.get_labels()
            self.get_centroids()

            if self.converges() == False and i< self.options['max_iter']:
               continua = True
            else:
                continua=False

            i = i+1




    def whitinClassDistance(self):
        """
         returns the whithin class distance of the current clustering
        """

        sumaTotal = 0
        i=0
        distancias = distance(self.X, self.centroids)

        while i < len(distancias):
            centroide = self.labels[i]
            distOptima = distancias[i][centroide]
            sumaTotal += pow(distOptima, 2)
            i=i+1
        resultado = sumaTotal / len(distancias)

        return resultado


    def find_bestK(self, max_K):
        """
         sets the best k anlysing the results up to 'max_K' clusters
        """

        anterior = 0
        k = 2
        while k < max_K:
            if k > 2:
                self.K = k
                self.fit()
                distancia = self.whitinClassDistance()

                percent = (distancia / anterior) * 100
                anterior = distancia

                if 100 - percent < 20:
                    self.K = k - 1
                    break

                elif k == max_K:
                    self.K = k
            else:
                self.K = k
                self.fit()
                anterior = self.whitinClassDistance()
            k = k + 1



def distance(X, C):
    """
    Calculates the distance between each pixcel and each centroid
    Args:
        X (numpy array): PxD 1st set of data points (usually data points)
        C (numpy array): KxD 2nd set of data points (usually cluster centroids points)

    Returns:
        dist: PxK numpy array position ij is the distance between the
        i-th point of the first set an the j-th point of the second set
    """


    ma = (X[:, np.newaxis] - C).reshape(-1,X.shape[1])

    ma= np.power(ma,2)
    ma = ma.sum(axis=1)
    ma = np.sqrt(ma)
    ma = ma.reshape(-1,C.shape[0])


    return ma

def get_colors(centroids):

    provabilitat = utils.get_color_prob(centroids)

    i = 0
    arg = np.argmax(provabilitat, axis=1)
    sn = np.array([])
    j= 0
    while j < len(utils.colors):

         if i<len(arg) and arg[i] == j:
            sn = np.append(sn, utils.colors[j])
            i = i + 1
            j = 0
         else: j=j+1

    return sn
