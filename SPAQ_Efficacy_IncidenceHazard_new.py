import pandas as pd
import seaborn as sns
from pylab import *

from dtk.utils.analyzers.BaseAnalyzer import BaseAnalyzer
from simtools.AnalyzeManager.AnalyzeManager import AnalyzeManager
from simtools.SetupParser import SetupParser

sns.set_style(style='white')
rc('mathtext', default='regular')

class IncidenceAnalyzer(BaseAnalyzer):
    filenames = ['output\\MalariaSummaryReport_DailyUnderFive.json']

    def __init__(self):
        super(IncidenceAnalyzer, self).__init__()
        self.reports = {}

    def apply(self, parser):
        if parser.experiment.exp_name not in self.reports:
            self.reports[parser.experiment.exp_name] = []

        self.reports[parser.experiment.exp_name].append(self.process_summary_report(parser.raw_data[self.filenames[0]]))

    def plot(self):
        fig_id = 1
        for exp_name, exp_reports in self.reports.items():
            fig = plt.figure(fig_id)
            fig.canvas.set_window_title(exp_name)

            ax = fig.add_subplot(111)
            df = pd.concat(exp_reports)

            grouped = df.groupby('day')
            means = grouped['cases'].aggregate(np.mean)
            low_boundary = grouped['cases'].aggregate(np.percentile, 2.5)
            high_boundary = grouped['cases'].aggregate(np.percentile, 97.5)

            ax.plot(range(len(means)), means, label=exp_name.split('-', 2)[2], lw=3)
            #ax.plot(range(len(means)), means, label=exp_name, lw=3)
            # ax.plot(range(len(means)), means, label=label, lw=3, color='k')
            ax.fill_between(range(len(high_boundary)), low_boundary, high_boundary, alpha=0.3)
            plt.legend(loc='upper left')
            ax.spines['top'].set_linewidth(0.5)
            ax.spines['top'].set_color("black")
            ax.spines['bottom'].set_linewidth(0.5)
            ax.spines['bottom'].set_color("black")
            ax.spines['left'].set_linewidth(0.5)
            ax.spines['left'].set_color("black")
            ax.spines['right'].set_linewidth(0.5)
            ax.spines['right'].set_color("black")
            plt.xlabel("Days since first SMC", fontsize=14, fontweight='bold')
            plt.ylabel("Cumulative incidence", fontsize=14, fontweight='bold')
            #plt.ylim(0, 1.2)
            plt.tick_params(labelsize=14)
            #fig_id += 1
            #fig_id = 1

        plt.show()

    def process_summary_report(self, data):
        #d = np.cumsum([i[0] / 365. for i in data['Annual Clinical Incidence by Age Bin']][230:230 + 120])
        d = np.cumsum([i[0] / 365. for i in data['DataByTimeAndAgeBins']['Annual Clinical Incidence by Age Bin']][230:230 + 120])
        df = pd.DataFrame({'cases': d,   'day': range(len(d))})

        return df

if __name__ == "__main__":
    from simtools.Utilities.Experiments import retrieve_experiment
    # 1. Make sure we have all the simulations in the DB
    exps = list()
    ####### Plots with input eir with latest eradication.exe
    # 0Round
    #exps.append(retrieve_experiment('93ea6c31-3560-e711-9401-f0921c16849d'))
    # 1Round
    #exps.append(retrieve_experiment('44921221-3560-e711-9401-f0921c16849d'))
    # 2Round
    #exps.append(retrieve_experiment('ed1ed212-3560-e711-9401-f0921c16849d'))
    # 3Round
    #exps.append(retrieve_experiment('60ac1e00-3560-e711-9401-f0921c16849d'))
    # 4Round
    #exps.append(retrieve_experiment('20ff60f2-3460-e711-9401-f0921c16849d'))

    ######## Plots with vectors eir with latest eradication.exe
    # 0Round
    #exps.append(retrieve_experiment('5a546d11-3660-e711-9401-f0921c16849d'))
    # 1Round
    #exps.append(retrieve_experiment('cb532a22-3660-e711-9401-f0921c16849d'))
    # 2Round
    #exps.append(retrieve_experiment('ca0c7336-3660-e711-9401-f0921c16849d'))
    # 3Round
    #exps.append(retrieve_experiment('8d23a244-3660-e711-9401-f0921c16849d'))
    # 4Round
    #exps.append(retrieve_experiment('b4725156-3660-e711-9401-f0921c16849d'))

    ####### Plots with vectors eir with latest eradication.exe Rate = 0, Seek = 1, Sweep Coverage
    # 0Round Cov = .3
    #exps.append(retrieve_experiment('ea2cb1e8-ee60-e711-9401-f0921c16849d'))
    # 0Round Cov = .5
    #exps.append(retrieve_experiment('4d18f382-ef60-e711-9401-f0921c16849d'))
    # 0Round Cov = .75
    #exps.append(retrieve_experiment('74db6cdc-ef60-e711-9401-f0921c16849d'))
    # 0Round Cov = 1
    #exps.append(retrieve_experiment('bfa4def0-ef60-e711-9401-f0921c16849d'))

    ####### Plots with vectors eir with latest eradication.exe Cov = 1., Seek = 1., Sweep Rate
    #Conclusion : No variation in Incidence rate which increased and remained consistent at a rate of ~2.3
    # 0Round Rate = .3
    #exps.append(retrieve_experiment('88d2db14-0461-e711-9401-f0921c16849d'))
    # 0Round Rate = .5
    #exps.append(retrieve_experiment('a8e33f25-0461-e711-9401-f0921c16849d'))
    # 0Round Rate = .75
    #exps.append(retrieve_experiment('987a4438-0461-e711-9401-f0921c16849d'))
    # 0Round Rate = 1
    #exps.append(retrieve_experiment('fc09984f-0461-e711-9401-f0921c16849d'))


    ####### Plots with vectors eir with latest eradication.exe Cov = .3, Rate = 0., Sweep Seek
    # 0Round Seek = .3
    exps.append(retrieve_experiment('dc6ef1f4-0861-e711-9401-f0921c16849d'))
    # 0Round Seek = .5
    exps.append(retrieve_experiment('2971800a-0961-e711-9401-f0921c16849d'))
    # 0Round Seek = .75
    exps.append(retrieve_experiment('a51c1d1c-0961-e711-9401-f0921c16849d'))
    # 0Round Seek = 1
    exps.append(retrieve_experiment('3df09b31-0961-e711-9401-f0921c16849d'))

    #Old plots for Gates review
    #exps.append(retrieve_experiment('3fb8ebc1-29cd-e611-93fe-f0921c168499'))
    #exps.append(retrieve_experiment('e489a1a3-29cd-e611-93fe-f0921c168499'))
    #exps.append(retrieve_experiment('118a2a45-29cd-e611-93fe-f0921c168499'))
    #exps.append(retrieve_experiment('65612e1a-29cd-e611-93fe-f0921c168499'))
    SetupParser.init('HPC')
    am = AnalyzeManager(exp_list=exps, analyzers=IncidenceAnalyzer())
    am.analyze()
