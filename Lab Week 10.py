import pandas
import scipy.stats
import numpy
import plotnine

class CI_simulation():
    
    def __init__(self):
        """Initializes the simulation"""
        self.dat = None
        self.mu = None
        self.ll_list = []
        self.ul_list = []
        self.coverage = None
        self.widths = []
        
    
    def gen_data(self, distribution, n):
        """
        Generate simulated data from the given distibution
        Parameters
        ----------
        distribution : String
            the name of the distribution to simulate from
            Can be one of the following:
                "norm"
                "uniform"
                "expon"
                "t" - t will have 10 df
        n : int > 1
            Size of the sample to simulate
        
        """
    
        if distribution == "norm":
            self.dat = pandas.Series(scipy.stats.norm.rvs(size = n))
            self.mu = scipy.stats.norm.mean()
        
        if distribution == "uniform":
            self.dat = pandas.Series(scipy.stats.uniform.rvs(size = n))
            self.mu = scipy.stats.uniform.mean()
            
            
        if distribution == "expon":
            self.dat = pandas.Series(scipy.stats.expon.rvs(size = n))
            self.mu = scipy.stats.expon.mean()
            
        if distribution == "t":
            self.dat = pandas.Series(scipy.stats.t.rvs(size = n, df = 10))
            self.mu = scipy.stats.t.mean(df = 10)
    



    def cal_conf_int(self, conf_level):
        """
        Calculates the specified level confidence interval for the given data
        Parameters
        ----------
        data : a pandas series
            The data used to make the confidence interval
        conf_level : float between 0 and 1 exclusive
            The confidence level of the interval for each iteration.
    
        Returns
        -------
        lower limit: float
            the lower limit of the interval
        upper limit: float
            the upper limit of the interval
        """
    
        n = len(self.dat)
        
        alpha = 1-conf_level
        t_cv = scipy.stats.t.ppf(1-alpha/2, n-1)
        
        xbar = self.dat.mean()
        std_dev = self.dat.std()
        ll = xbar - t_cv*(std_dev/numpy.sqrt(n))
        ul = xbar + t_cv*(std_dev/numpy.sqrt(n))
        
        return ll, ul




    def conf_int_sim(self, distribution, n, conf_level, num_sims):
        """
        Simulates data from distribution and computes the confidence interval. 
        This is done num_sims times. The coverage of the interval is returned
    
        Parameters
        ----------
        distribution : String
            the name of the distribution to simulate from
            Can be one of the following:
                "norm"
                "uniform"
                "expon"
                "t" - t will have 10 df
        n : int > 1
            Size of the sample to simulate
        conf_level : float between 0 and 1 exclusive
            The confidence level of the interval for each iteration.
        num_sims : int > 0
            The number of iterations.
    
        Returns
        -------
        A float representing the proportion of times the interval contained the
        true mean.
    
        """
        
        for i in range(num_sims):
            self.gen_data( distribution, n)
            ll, ul = self.cal_conf_int( conf_level)
            self.ll_list.append(ll)
            self.ul_list.append(ul)
            self.widths.append(ul - ll)
            
            
        coverage_list = [self.mu>x and self.mu<y for x,y in zip(self.ll_list, self.ul_list)]
        self.coverage = numpy.mean(coverage_list)
        
        return self.coverage
    

            
    
    def widths_histogram(self):
        widths_df = pandas.DataFrame(self.widths, columns = ["widths"])
        
        p = (
            plotnine.ggplot(widths_df)+
            plotnine.aes(x = "widths")+          
            plotnine.geom_histogram(color = "black", fill = "red")
         
         )
        return p


test = CI_simulation()
test.conf_int_sim("norm", 100, .95, 10000)
test.widths_histogram()
