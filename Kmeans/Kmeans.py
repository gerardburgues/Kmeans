__authors__ = ['1493112','1392437', '1420576']
__group__ = 'DL.15'

import numpy as np
import utils
import random


class KMeans:

    def __init__(self, X, K=1, options=None):
        """
         Constructor of KMeans class
             Args:
                 K (int): Number of cluster
                 options (dict): dictºionary with options
            """
        self.num_iter = 0
        self.K = K
        self._init_X(X)
        self._init_options(options)  # DICT options

    #############################################################
    ##  THIS FUNCTION CAN BE MODIFIED FROM THIS POINT, if needed
    #############################################################






    def _init_X(self, X):

        #self.X = np.random.rand(100, 5)
        # Assegurem que tots els valors siguin del tipus float
        np.dtype(float)
        rows =len(X)
        colum= len(X[-1])
      #  print(rows,colum)
        N = rows * colum
        #condició
        if X.ndim > 2:
            #s'ha de modificar el reshape per que no funciona
            self.X = np.reshape(X,(N ,X.shape[-1]))


    def _init_options(self, options=None):
        """
        Initialization of options in case some fields are left undefined
        Args:
            options (dict): dictionary with options
        """
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

        # If your methods need any other prameter you can add it to the options dictionary
        self.options = options

        #############################################################
        ##  THIS FUNCTION CAN BE MODIFIED FROM THIS POINT, if needed
        #############################################################




    def _init_centroids(self):

        if self.options['km_init'].lower() == 'first':
            #u devuelve una matriz ordenada por columnas X
            # idx printa els index de cada matriu anteriorment mostrada per u
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

            #print(x)
            i=i+1

        self.centroids = x.reshape(-1,self.X.shape[1])


        #print("suma final", self.centroids)


    def converges(self):
        """
        Checks if there is a difference between current and old centroids
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################
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

        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################
          # Ho estem fent amb init centroids!!!!!!!!!!!!



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
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################
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

    #########################################################
    ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
    ##  AND CHANGE FOR YOUR OWN CODE
    #########################################################


    ma = (X[:, np.newaxis] - C).reshape(-1,X.shape[1])

    ma= np.power(ma,2)
    ma = ma.sum(axis=1)
    ma = np.sqrt(ma)
    ma = ma.reshape(-1,C.shape[0])


   # print("esto es bullshit", ma)
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
