from reader import generate_tab_files
from Empire import run_empire
from scenario_random import generate_random_scenario
from datetime import datetime
import time
import gc

########
##USER##
########

USE_TEMP_DIR = True #True/False
temp_dir = '/mnt/beegfs/users/gorand/TempDir'
version = 'hydrogenAllCountries'
NoOfPeriods = 8
NoOfScenarios = 3
NoOfRegSeason = 4
lengthRegSeason = 168
regular_seasons = ["winter", "spring", "summer", "fall"]
NoOfPeakSeason = 2
lengthPeakSeason = 24
discountrate = 0.05
WACC = 0.05
LeapYearsInvestment = 5
solver = "Gurobi" #"Gurobi" #"CPLEX" #"Xpress"
scenariogeneration = False #True #False
EMISSION_CAP = True #False
WRITE_LP = False #True
PICKLE_INSTANCE = False #True 
hydrogen = True
hydrogenPercentages = [0] #Make it a whole number, this is divided by 100 later to make it a fraction between 0 and 1
h2storage = False
TIME_LIMIT = 0

#######
##RUN##
#######
for hydrogenPercentage in hydrogenPercentages:
    print(f'Hydrogen 1: {str(hydrogen)}')
    name = version + "_H2Percentage" + str(hydrogenPercentage)

    workbook_path = 'Data handler/' + version
    tab_file_path = 'Data handler/' + version + '/Tab_Files_' + name
    scenario_data_path = 'Data handler/' + version + '/ScenarioData'
    result_file_path = 'Results/' + version + '/' + name
    FirstHoursOfRegSeason = [lengthRegSeason*i + 1 for i in range(NoOfRegSeason)]
    FirstHoursOfPeakSeason = [lengthRegSeason*NoOfRegSeason + lengthPeakSeason*i + 1 for i in range(NoOfPeakSeason)]
    Period = [i + 1 for i in range(NoOfPeriods)]
    Scenario = ["scenario"+str(i + 1) for i in range(NoOfScenarios)]
    peak_seasons = ['peak'+str(i + 1) for i in range(NoOfPeakSeason)]
    Season = regular_seasons + peak_seasons
    Operationalhour = [i + 1 for i in range(FirstHoursOfPeakSeason[-1] + lengthPeakSeason - 1)]
    HoursOfRegSeason = [(s,h) for s in regular_seasons for h in Operationalhour \
                     if h in list(range(regular_seasons.index(s)*lengthRegSeason+1,
                                   regular_seasons.index(s)*lengthRegSeason+lengthRegSeason+1))]
    HoursOfPeakSeason = [(s,h) for s in peak_seasons for h in Operationalhour \
                         if h in list(range(lengthRegSeason*len(regular_seasons)+ \
                                            peak_seasons.index(s)*lengthPeakSeason+1,
                                            lengthRegSeason*len(regular_seasons)+ \
                                                peak_seasons.index(s)*lengthPeakSeason+ \
                                                    lengthPeakSeason+1))]
    HoursOfSeason = HoursOfRegSeason + HoursOfPeakSeason
    dict_countries = {"AT": "Austria", "BA": "BosniaH", "BE": "Belgium",
                      "BG": "Bulgaria", "CH": "Switzerland", "CZ": "CzechR",
                      "DE": "Germany", "DK": "Denmark", "EE": "Estonia",
                      "ES": "Spain", "FI": "Finland", "FR": "France",
                      "GB": "GreatBrit.", "GR": "Greece", "HR": "Croatia",
                      "HU": "Hungary", "IE": "Ireland", "IT": "Italy",
                      "LT": "Lithuania", "LU": "Luxemb.", "LV": "Latvia",
                      "MK": "Macedonia", "NL": "Netherlands", "NO": "Norway",
                      "PL": "Poland", "PT": "Portugal", "RO": "Romania",
                      "RS": "Serbia", "SE": "Sweden", "SI": "Slovenia",
                      "SK": "Slovakia", "MF": "MorayFirth", "FF": "FirthofForth",
                      "DB": "DoggerBank", "HS": "Hornsea", "OD": "OuterDowsing",
                      "NF": "Norfolk", "EA": "EastAnglia", "BS": "Borssele",
                      "HK": "HollandseeKust", "HB": "HelgoländerBucht", "NS": "Nordsøen",
                      "UN": "UtsiraNord", "SN1": "SørligeNordsjøI", "SN2": "SørligeNordsjøII",
                      "EHGB":"Energyhub Great Britain", "EHNO": "Energyhub Norway",
                      "EHEU": "Energyhub EU"}
    offshoreNodesList = ["Energyhub Great Britain", "Energyhub Norway", "Energyhub EU"]
    windfarmNodes = ["Moray Firth","Firth of Forth","Dogger Bank","Hornsea","Outer Dowsing","Norfolk","East Anglia","Borssele","Hollandsee Kust","Helgoländer Bucht","Nordsøen","Utsira Nord","Sørlige Nordsjø I","Sørlige Nordsjø II"]
    print(f'Hydrogen 2: {str(hydrogen)}')
    if hydrogen is True and hydrogenPercentage == 0:
        hydrogen = False
    print(f'Hydrogen 3: {str(hydrogen)}')

    print('++++++++')
    print('+EMPIRE+')
    print('++++++++')
    print('Solver: ' + solver)
    print('Scenario Generation: ' + str(scenariogeneration))
    print('++++++++')
    print('ID: ' + name)
    print('++++++++')
    print('Hydrogen: ' + str(hydrogen))
    print('++++++++')


    if scenariogeneration:
        tick = time.time()
        generate_random_scenario(filepath = scenario_data_path,
                                 tab_file_path = tab_file_path,
                                 scenarios = NoOfScenarios,
                                 seasons = regular_seasons,
                                 Periods = NoOfPeriods,
                                 regularSeasonHours = lengthRegSeason,
                                 peakSeasonHours = lengthPeakSeason,
                                 dict_countries = dict_countries)
        tock = time.time()
        print("{hour}:{minute}:{second}: Scenario generation took [sec]:".format(
		hour=datetime.now().strftime("%H"), minute=datetime.now().strftime("%M"), second=datetime.now().strftime("%S")) + str(tock - tick))

    generate_tab_files(filepath = workbook_path, tab_file_path = tab_file_path,
                       scenariogeneration = scenariogeneration, hydrogen = hydrogen)

    run_empire(name = name,
               tab_file_path = tab_file_path,
               result_file_path = result_file_path,
               scenariogeneration = scenariogeneration,
               scenario_data_path = scenario_data_path,
               solver = solver,
               temp_dir = temp_dir,
               FirstHoursOfRegSeason = FirstHoursOfRegSeason,
               FirstHoursOfPeakSeason = FirstHoursOfPeakSeason,
               lengthRegSeason = lengthRegSeason,
               lengthPeakSeason = lengthPeakSeason,
               Period = Period,
               Operationalhour = Operationalhour,
               Scenario = Scenario,
               Season = Season,
               HoursOfSeason = HoursOfSeason,
               discountrate = discountrate,
               WACC = WACC,
               LeapYearsInvestment = LeapYearsInvestment,
               WRITE_LP = WRITE_LP,
               PICKLE_INSTANCE = PICKLE_INSTANCE,
               EMISSION_CAP = EMISSION_CAP,
               USE_TEMP_DIR = USE_TEMP_DIR,
               NoOfRegSeason = NoOfRegSeason,
               NoOfPeakSeason = NoOfPeakSeason,
               offshoreNodesList = offshoreNodesList,
               verboseResultWriting = False,
               hydrogen = hydrogen,
               hydrogenPercentage = hydrogenPercentage/100,
               TIME_LIMIT = TIME_LIMIT,
               h2storage = h2storage,
               windfarmNodes = windfarmNodes,
               reformMaxCapFac=0)
    gc.collect()