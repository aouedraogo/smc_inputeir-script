from dtk.utils.core.DTKConfigBuilder import DTKConfigBuilder
from dtk.vector.study_sites import configure_site
from simtools.ExperimentManager import ExperimentManagerFactory
from simtools.SetupParser import SetupParser
from dtk.vector.species import set_larval_habitat
from dtk.utils.reports.MalariaReport import add_summary_report
from dtk.utils.reports.MalariaReport import add_patient_report
from dtk.interventions.health_seeking import add_health_seeking 
from dtk.interventions.malaria_drug_campaigns import add_drug_campaign
from dtk.utils.builders.sweep import GenericSweepBuilder

from dtk.vector.input_EIR_by_site import configure_site_EIR
# HS means Health Seeking "coverage" parameter and not "seek" parameter
expname = 'newsmcexp09_vectorseir-burnin_smcSPA_0R_Sweep-Seek1.-Rate.0-Cov.3'
#First sim: expname = 'newsmcexp01_5yr_SPA_CM1.SEEK1.Rate1.CampStartDay230_4R_sweep'
#expname = 'newsmcexp01_5yr_SPA_CM0.SEEK0.Rate0.CampStartDay230_4R_sweep1'
#expname = 'newsmcexp03_50yrburnin_SPA_5yrsim_StartDay230_0R_Sweep'
#expname = '50yr-serial_burkina_site_vectors_03'


cb = DTKConfigBuilder.from_defaults('MALARIA_SIM')

#configure_site_EIR(cb, 'Dapelogo', birth_cohort = False)

configure_site(cb, 'Dapelogo')

cb.update_params( {"Geography": "Burkina",
                   #"Demographics_Filename": "Burkina/Burkina/Burkina Faso_Dapelogo_2.5arcmin_demographics.json",
                   #"Air_Temperature_Filename": "Burkina/Burkina/fiveyear/Burkina Faso_Burkina Faso_2.5arcmin_air_temperature_daily.bin",
                   #"Land_Temperature_Filename": "Burkina/Burkina/fiveyear/Burkina Faso_Burkina Faso_2.5arcmin_air_temperature_daily.bin",
                   #"Rainfall_Filename": "Burkina/Burkina/fiveyear/Burkina Faso_Burkina Faso_2.5arcmin_rainfall_daily.bin",
                   #"Relative_Humidity_Filename": "Burkina/Burkina/fiveyear/Burkina Faso_Burkina Faso_2.5arcmin_relative_humidity_daily.bin",
                   "Enable_Climate_Stochasticity": 0,  
                   "Simulation_Duration" : 365*1,
                   "Vector_Species_Names" : ["gambiae", "funestus"],
                   #"Serialization_Time_Steps" : [50*365],
                   "Serialized_Population_Path": "//Idmppfil01/idm/home/aouedraogo/output/50yr-serial_burkina_site_vectors_03_2017_07_03_10_48_21_887000/741/d98/ea1/741d98ea-1760-e711-9401-f0921c16849d/output/",
                   "Serialized_Population_Filenames": ["state-18250.dtk"],
                   "Birth_Rate_Dependence" : "FIXED_BIRTH_RATE",
                   "Enable_Nondisease_Mortality" : 1,
                   "Enable_Vital_Dynamics" : 1,
                   "Listed_Events" : ["Received_Treatment", 'Received_Campaign_Drugs'],
                   "logLevel_ReportUtilities" : "ERROR",
				   "Report_Event_Recorder" : 0,
				   "Report_Event_Recorder_Events" : ['Received_Treatment', 'NewClinicalCase'], 
				   "Report_Event_Recorder_Ignore_Events_In_List" : 0, 
				   
} )


#add_summary_report(cb)
#add_patient_report(cb)
# add_health_seeking(cb, start_day=0, drug=['Lumefantrine', 'Artemether'],
#                    targets=[{'trigger': 'NewClinicalCase', 'coverage': .33, 'agemin': 0, 'agemax': 5, 'seek': 1,
#                              'rate': 0.3}, {'trigger': 'NewClinicalCase', 'coverage': .33, 'agemin': 5, 'agemax': 200, 'seek': 1,
#                              'rate': 0.3}])

add_health_seeking(cb, start_day=0, drug=['Lumefantrine', 'Artemether'],
                   targets=[{'trigger': 'NewClinicalCase', 'coverage': .3, 'agemin': 0, 'agemax': 5, 'seek': 1.,
                             'rate': 0.}, {'trigger': 'NewClinicalCase', 'coverage': 1., 'agemin': 5, 'agemax': 200, 'seek': 1.,
                             'rate': 0.}])



#add_drug_campaign(cb, "SMC", "SPA", start_days=[230 + 365*x for x in range(5)], repetitions=4, interval=30, coverage=1., target_group={'agemin' : 0, 'agemax' : 5})


add_summary_report(cb, interval=365/12., description='Monthly', age_bins=[5, 15, 200])
#add_summary_report(cb, interval=365/12., description='MonthlyUnderFive', age_bins=[5])
add_summary_report(cb, interval=1., description='DailyUnderFive', age_bins=[5, 15, 200])
#add_summary_report(cb, interval=365/12., description='AnnualUnderFive', age_bins=[5])

#builder = GenericSweepBuilder.from_dict({'Run_Number':range(1)})
builder = GenericSweepBuilder.from_dict({'Run_Number':range(100)})

run_sim_args =  {'config_builder': cb,
                 'exp_name': expname,
                 'exp_builder':builder}


if __name__ == "__main__":
    sm = ExperimentManagerFactory.from_setup(SetupParser())
    sm.run_simulations(**run_sim_args)
