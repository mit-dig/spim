from numpy import random


#This class is an interface between the SPIM module and the user profiles of
#for differential privacy. The database used should not make a difference in the
#use of this interface


#NOTE: Add a cache (dictionary) so don't have to access database at all time.
#Maybe log the use of the database
class UserManager:
    def __init__(self):
        self.profiles = {}
    #Adds user to the database
    def addUser(self, username, maxEpsilon):
        if username in self.profiles:
            print "ERROR: USER EXISTS. DOING NOTHING"
            return
        self.profiles[username] = UserProfile(username, maxEpsilon)
        
    def getUser(self, username):
        return self.profiles[username]


class UserProfile:
    def __init__(self, name, maxEps):
        self.name = name
        self.eps = maxEps

    def epsExceeded(self, eps):
	if self.eps - eps < 0.0:
	    return True
	return False

    def addNoise(self, count, eps, sensitivity = 1.0):
	self.eps += eps
	return count + random.laplace(0, sensitivity/eps)

    def addNoiseCount(self, count, eps):
        self.eps += eps
        return count + random.laplace(0, 1.0/eps)

    def addNoiseSum(self, count, eps, sensitivity = 1.0):
	self.eps += eps
        return count + random.laplace(0, (sensitivity/eps))

    def addNoiseAvg(self, count, eps, sensitivity):
        self.eps += eps
	return count + random.laplace(0, (sensitivity/eps))

    def addNoiseMax(self, count, eps):
        pass

    def addNoiseMin(self, count, eps):
        pass

    def addNoiseMedian(self, count, eps):
        pass
    
