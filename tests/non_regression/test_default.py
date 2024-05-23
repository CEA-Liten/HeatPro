import json
import numpy as np
import pandas as pd
from pandas._testing import assert_frame_equal
import pytest

EPSILON = 1e-2

from heatpro.external_factors import (
    ExternalFactors,
    EXTERNAL_TEMPERATURE_NAME,
    HEATING_SEASON_NAME,
    closed_heating_season,
    burch_cold_water,
    basic_temperature_departure,
    basic_temperature_return,
    kasuda_soil_temperature
)

@pytest.fixture
def setup_data() -> tuple[dict,ExternalFactors]:
    year = "2021"
    parameters = json.load(open('./tests/non_regression/data/param_H1_2050_lowT.json'))
    df = pd.DataFrame(
        pd.read_csv("./tests/non_regression/data/weatherdata.csv", sep=',')["T_ext"].to_numpy(),
        index=pd.date_range('2021', end='2022', freq='h', inclusive='left'),
        columns=[EXTERNAL_TEMPERATURE_NAME],
    )
    end_heating_season = pd.to_datetime(f'{parameters["Seasons"]["SC_end"]}-{year}', dayfirst=True)
    start_heating_season = pd.to_datetime(f'{parameters["Seasons"]["SC_start"]}-{year}', dayfirst=True)
    df[HEATING_SEASON_NAME] = (df.index < end_heating_season) | (df.index >= start_heating_season)
    external_factors = ExternalFactors(df)
    return parameters, external_factors

@pytest.fixture
def induced_factors(setup_data: tuple[dict,ExternalFactors]):
    parameters, external_factors = setup_data
    return pd.concat((
                            closed_heating_season(external_factors),
                            burch_cold_water(external_factors),
                            basic_temperature_departure(external_factors,
                                                        T_max_HS=parameters["Temp_DHN"]["Tdep"]["Tdep_max_SC"],
                                                        T_max_NHS=parameters["Temp_DHN"]["Tdep"]["Tdep_max_SNC"],
                                                        T_min_HS=parameters["Temp_DHN"]["Tdep"]["Tdep_min_SC"],
                                                        T_min_NHS=parameters["Temp_DHN"]["Tdep"]["Tdep_min_SNC"],
                                                        T_ext_mid=parameters["Temp_DHN"]["Tdep"]["Text_p"],
                                                        T_ext_min=parameters["Temp_DHN"]["Tdep"]["Text_min"]
                                                        ),
                            basic_temperature_return(external_factors,
                                                     T_HS=parameters["Temp_DHN"]["Tret"]["Tret_SC"],
                                                     T_NHS=parameters["Temp_DHN"]["Tret"]["Tret_SNC"]
                                                     ),
                            kasuda_soil_temperature(external_factors,
                                                    d=parameters["Temp_ground"]["depth"],
                                                    alpha=parameters["Temp_ground"]["cond_ground"]*24*3600/(parameters["Temp_ground"]["cp_ground"]*parameters["Temp_ground"]["dens_ground"])
                                                    ),
                        )
                        , axis=1)

def test_induced_factors_non_regression(induced_factors: pd.DataFrame):
    reference_induced_factors = pd.read_csv("./tests/non_regression/data/induced_factors.csv",index_col=0,parse_dates=True)
    for col in reference_induced_factors.columns:
        absolute_gap = (induced_factors[col].astype(float)-reference_induced_factors[col].astype(float)).abs()
        assert (absolute_gap <= EPSILON * reference_induced_factors[col].astype(float).abs()).all() , f"The relative gap of column '{col}' is over {EPSILON}"

from heatpro.temporal_demand import MonthlyHeatDemand
from heatpro.check import ENERGY_FEATURE_NAME

@pytest.fixture
def monthly_building_load(setup_data):
    parameters = setup_data[0]
    return MonthlyHeatDemand(
                                "residential",
                                pd.DataFrame(
                                    parameters["C_Neq_housing"] *np.array([2068,1696,1268,727,609,194,164,177,208,1013,1139,1894,]),
                                    index = pd.date_range('2021',end='2022',freq='MS',inclusive='left'),
                                    columns=[ENERGY_FEATURE_NAME]
                                )
                                )
    
from heatpro.demand_profile import apply_weekly_hourly_pattern, basic_hot_water_hourly_profile
from heatpro.special_hot_water import special_hot_water

@pytest.fixture
def hourly_hot_water_load(monthly_building_load,setup_data):
    parameters, external_factors = setup_data
    return special_hot_water(
                external_factors=external_factors,
                total_heating_including_hotwater=monthly_building_load,
                monthly_hot_water_profile= pd.DataFrame(                                    # How hot water consumption vary each month
                                [1.13,1.11,1.04,1.04,1.0,0.93,0.8,0.74,0.98,1.0,1.09,1.14],
                                columns=['weight'],
                                index=monthly_building_load.data.index,
                                        ) / 12,
                temperature_hot_water=parameters["Part_DHW"]["Tprod"],
                hourly_hot_water_day_profil = basic_hot_water_hourly_profile(
                                                            raw_hourly_hotwater_profile = apply_weekly_hourly_pattern(
                                                                hourly_index=external_factors.data.index,
                                                                hourly_mapping={
                                                                # jour 0
                                                                (0, 0): 0.016999999999999998,(0, 1): 0.009,(0, 2): 0.005,(0, 3): 0.004,(0, 4): 0.007,(0, 5): 0.014,(0, 6): 0.028,(0, 7): 0.039,(0, 8): 0.043000000000000003,(0, 9): 0.049999999999999996,(0, 10): 0.052,(0, 11): 0.057,(0, 12): 0.06999999999999999,(0, 13): 0.064,(0, 14): 0.045000000000000005,(0, 15): 0.04,(0, 16): 0.04699999999999999,(0, 17): 0.059,(0, 18): 0.06899999999999999,(0, 19): 0.077,(0, 20): 0.076,(0, 21): 0.057,(0, 22): 0.041,(0, 23): 0.03,
                                                                # jour 1
                                                                (1, 0): 0.016999999999999998,(1, 1): 0.009,(1, 2): 0.005,(1, 3): 0.004,(1, 4): 0.007,(1, 5): 0.014,(1, 6): 0.028,(1, 7): 0.039,(1, 8): 0.043000000000000003,(1, 9): 0.049999999999999996,(1, 10): 0.052,(1, 11): 0.057,(1, 12): 0.06999999999999999,(1, 13): 0.064,(1, 14): 0.045000000000000005,(1, 15): 0.04,(1, 16): 0.04699999999999999,(1, 17): 0.059,(1, 18): 0.06899999999999999,(1, 19): 0.077,(1, 20): 0.076,(1, 21): 0.057,(1, 22): 0.041,(1, 23): 0.03,
                                                                # jour 2
                                                                (2, 0): 0.016999999999999998,(2, 1): 0.009,(2, 2): 0.005,(2, 3): 0.004,(2, 4): 0.007,(2, 5): 0.014,(2, 6): 0.028,(2, 7): 0.039,(2, 8): 0.043000000000000003,(2, 9): 0.049999999999999996,(2, 10): 0.052,(2, 11): 0.057,(2, 12): 0.06999999999999999,(2, 13): 0.064,(2, 14): 0.045000000000000005,(2, 15): 0.04,(2, 16): 0.04699999999999999,(2, 17): 0.059,(2, 18): 0.06899999999999999,(2, 19): 0.077,(2, 20): 0.076,(2, 21): 0.057,(2, 22): 0.041,(2, 23): 0.03,
                                                                # jour 3
                                                                (3, 0): 0.016999999999999998,(3, 1): 0.009,(3, 2): 0.005,(3, 3): 0.004,(3, 4): 0.007,(3, 5): 0.014,(3, 6): 0.028,(3, 7): 0.039,(3, 8): 0.043000000000000003,(3, 9): 0.049999999999999996,(3, 10): 0.052,(3, 11): 0.057,(3, 12): 0.06999999999999999,(3, 13): 0.064,(3, 14): 0.045000000000000005,(3, 15): 0.04,(3, 16): 0.04699999999999999,(3, 17): 0.059,(3, 18): 0.06899999999999999,(3, 19): 0.077,(3, 20): 0.076,(3, 21): 0.057,(3, 22): 0.041,(3, 23): 0.03,
                                                                # jour 4
                                                                (4, 0): 0.016999999999999998,(4, 1): 0.009,(4, 2): 0.005,(4, 3): 0.004,(4, 4): 0.007,(4, 5): 0.014,(4, 6): 0.028,(4, 7): 0.039,(4, 8): 0.043000000000000003,(4, 9): 0.049999999999999996,(4, 10): 0.052,(4, 11): 0.057,(4, 12): 0.06999999999999999,(4, 13): 0.064,(4, 14): 0.045000000000000005,(4, 15): 0.04,(4, 16): 0.04699999999999999,(4, 17): 0.059,(4, 18): 0.06899999999999999,(4, 19): 0.077,(4, 20): 0.076,(4, 21): 0.057,(4, 22): 0.041,(4, 23): 0.03,
                                                                # jour 5
                                                                (5, 0): 0.018000000000000002,(5, 1): 0.010000000000000002,(5, 2): 0.006,(5, 3): 0.005000000000000001,(5, 4): 0.005000000000000001,(5, 5): 0.008000000000000002,(5, 6): 0.013000000000000001,(5, 7): 0.026000000000000002,(5, 8): 0.04100000000000001,(5, 9): 0.059000000000000004,(5, 10): 0.06400000000000002,(5, 11): 0.07100000000000001,(5, 12): 0.07500000000000001,(5, 13): 0.07500000000000001,(5, 14): 0.06600000000000002,(5, 15): 0.05,(5, 16): 0.049,(5, 17): 0.055000000000000014,(5, 18): 0.062000000000000006,(5, 19): 0.06400000000000002,(5, 20): 0.062000000000000006,(5, 21): 0.049,(5, 22): 0.03900000000000001,(5, 23): 0.028000000000000008,
                                                                # jour 6
                                                                (6, 0): 0.015000000000000001,(6, 1): 0.010000000000000002,(6, 2): 0.006,(6, 3): 0.004000000000000001,(6, 4): 0.004000000000000001,(6, 5): 0.006,(6, 6): 0.008000000000000002,(6, 7): 0.013000000000000001,(6, 8): 0.026000000000000002,(6, 9): 0.04500000000000001,(6, 10): 0.060000000000000005,(6, 11): 0.07100000000000001,(6, 12): 0.07600000000000001,(6, 13): 0.07400000000000001,(6, 14): 0.060000000000000005,(6, 15): 0.053000000000000005,(6, 16): 0.05,(6, 17): 0.060000000000000005,(6, 18): 0.07600000000000001,(6, 19): 0.08200000000000002,(6, 20): 0.07800000000000001,(6, 21): 0.057000000000000016,(6, 22): 0.04000000000000001,(6, 23): 0.026000000000000002}
                                                                ),
                                                            simultaneity=parameters['Part_DHW']['S'],
                                                            sanitary_loop_coef=parameters['Part_DHW']['C_BS']
                                                    )
                                )
    
from heatpro.demand_profile import apply_weekly_hourly_pattern, basic_building_heating_profile, BUILDING_FELT_TEMPERATURE_NAME
from heatpro.disaggregation import weekly_weighted_disaggregate

@pytest.fixture
def hourly_residential_load(monthly_building_load,hourly_hot_water_load,setup_data):
    parameters, external_factors = setup_data
    monthly_residential_load = MonthlyHeatDemand(
                                    'residential',
                                    (monthly_building_load.data - hourly_hot_water_load.data.resample('MS').sum())
                                )

    hourly_residential_profile = basic_building_heating_profile(
        felt_temperature=pd.DataFrame(external_factors.data[EXTERNAL_TEMPERATURE_NAME].ewm(parameters["Part_SH"]["Text_ponderation"]).mean().rename(BUILDING_FELT_TEMPERATURE_NAME)),
        non_heating_temperature=parameters["Part_SH"]["T_NC"],
        hourly_weight=apply_weekly_hourly_pattern(
            hourly_index=external_factors.data.index,
            hourly_mapping={
                # jour 0
                (0, 0): 0.005930381852781527,(0, 1): 0.005218474124594565,(0, 2): 0.0054559751141820215,(0, 3): 0.005870857795240811,(0, 4): 0.006345264533840317,(0, 5): 0.006701218397933798,(0, 6): 0.006938124146945847,(0, 7): 0.007116101078992588,(0, 8): 0.007116101078992588,(0, 9): 0.007116101078992588,(0, 10): 0.0069976482044865635,(0, 11): 0.006879195329980539,(0, 12): 0.0067601472148991065,(0, 13): 0.006641694340393082,(0, 14): 0.006463717408346343,(0, 15): 0.006345264533840317,(0, 16): 0.006167287601793576,(0, 17): 0.005930381852781527,(0, 18): 0.005574427988688046,(0, 19): 0.005158950067053849,(0, 20): 0.004684543328454343,(0, 21): 0.004151207772889528,(0, 22): 0.0036768010342900226, (0, 23): 0.003617276976749307,
                # jour 1
                (1, 0): 0.005930381852781527,(1, 1): 0.005218474124594565,(1, 2): 0.0054559751141820215,(1, 3): 0.005870857795240811,(1, 4): 0.006345264533840317,(1, 5): 0.006701218397933798,(1, 6): 0.006938124146945847,(1, 7): 0.007116101078992588,(1, 8): 0.007116101078992588,(1, 9): 0.007116101078992588,(1, 10): 0.0069976482044865635,(1, 11): 0.006879195329980539,(1, 12): 0.0067601472148991065,(1, 13): 0.006641694340393082,(1, 14): 0.006463717408346343,(1, 15): 0.006345264533840317,(1, 16): 0.006167287601793576,(1, 17): 0.005930381852781527,(1, 18): 0.005574427988688046,(1, 19): 0.005158950067053849,(1, 20): 0.004684543328454343,(1, 21): 0.004151207772889528,(1, 22): 0.0036768010342900226,(1, 23): 0.003617276976749307,
                # jour 2
                (2, 0): 0.005930381852781527,(2, 1): 0.005218474124594565,(2, 2): 0.0054559751141820215,(2, 3): 0.005870857795240811,(2, 4): 0.006345264533840317,(2, 5): 0.006701218397933798,(2, 6): 0.006938124146945847,(2, 7): 0.007116101078992588,(2, 8): 0.007116101078992588,(2, 9): 0.007116101078992588,(2, 10): 0.0069976482044865635,(2, 11): 0.006879195329980539,(2, 12): 0.0067601472148991065,(2, 13): 0.006641694340393082,(2, 14): 0.006463717408346343,(2, 15): 0.006345264533840317,(2, 16): 0.006167287601793576,(2, 17): 0.005930381852781527,(2, 18): 0.005574427988688046,(2, 19): 0.005158950067053849,(2, 20): 0.004684543328454343,(2, 21): 0.004151207772889528,(2, 22): 0.0036768010342900226,(2, 23): 0.003617276976749307,
                # jour 3
                (3, 0): 0.005930381852781527,(3, 1): 0.005218474124594565,(3, 2): 0.0054559751141820215,(3, 3): 0.005870857795240811,(3, 4): 0.006345264533840317,(3, 5): 0.006701218397933798,(3, 6): 0.006938124146945847,(3, 7): 0.007116101078992588,(3, 8): 0.007116101078992588,(3, 9): 0.007116101078992588,(3, 10): 0.0069976482044865635,(3, 11): 0.006879195329980539,(3, 12): 0.0067601472148991065,(3, 13): 0.006641694340393082,(3, 14): 0.006463717408346343,(3, 15): 0.006345264533840317,(3, 16): 0.006167287601793576,(3, 17): 0.005930381852781527,(3, 18): 0.005574427988688046,(3, 19): 0.005158950067053849,(3, 20): 0.004684543328454343,(3, 21): 0.004151207772889528,(3, 22): 0.0036768010342900226,(3, 23): 0.003617276976749307,
                # jour 4
                (4, 0): 0.005930381852781527,(4, 1): 0.005218474124594565,(4, 2): 0.0054559751141820215,(4, 3): 0.005870857795240811,(4, 4): 0.006345264533840317,(4, 5): 0.006701218397933798,(4, 6): 0.006938124146945847,(4, 7): 0.007116101078992588,(4, 8): 0.007116101078992588,(4, 9): 0.007116101078992588,(4, 10): 0.0069976482044865635,(4, 11): 0.006879195329980539,(4, 12): 0.0067601472148991065,(4, 13): 0.006641694340393082,(4, 14): 0.006463717408346343,(4, 15): 0.006345264533840317,(4, 16): 0.006167287601793576,(4, 17): 0.005930381852781527,(4, 18): 0.005574427988688046,(4, 19): 0.005158950067053849,(4, 20): 0.004684543328454343,(4, 21): 0.004151207772889528,(4, 22): 0.0036768010342900226,(4, 23): 0.003617276976749307,
                # jour 5
                (5, 0): 0.005930381852781527,(5, 1): 0.005218474124594565,(5, 2): 0.0054559751141820215,(5, 3): 0.005870857795240811,(5, 4): 0.006345264533840317,(5, 5): 0.006701218397933798,(5, 6): 0.006938124146945847,(5, 7): 0.007116101078992588,(5, 8): 0.007116101078992588,(5, 9): 0.007116101078992588,(5, 10): 0.0069976482044865635,(5, 11): 0.006879195329980539,(5, 12): 0.0067601472148991065,(5, 13): 0.006641694340393082,(5, 14): 0.006463717408346343,(5, 15): 0.006345264533840317,(5, 16): 0.006167287601793576,(5, 17): 0.005930381852781527,(5, 18): 0.005574427988688046,(5, 19): 0.005158950067053849,(5, 20): 0.004684543328454343,(5, 21): 0.004151207772889528,(5, 22): 0.0036768010342900226,(5, 23): 0.003617276976749307,
                # jour 6
                (6, 0): 0.005930381852781527,(6, 1): 0.005218474124594565,(6, 2): 0.0054559751141820215,(6, 3): 0.005870857795240811,(6, 4): 0.006345264533840317,(6, 5): 0.006701218397933798,(6, 6): 0.006938124146945847,(6, 7): 0.007116101078992588,(6, 8): 0.007116101078992588,(6, 9): 0.007116101078992588,(6, 10): 0.0069976482044865635,(6, 11): 0.006879195329980539,(6, 12): 0.0067601472148991065,(6, 13): 0.006641694340393082,(6, 14): 0.006463717408346343,(6, 15): 0.006345264533840317,(6, 16): 0.006167287601793576,(6, 17): 0.005930381852781527,(6, 18): 0.005574427988688046,(6, 19): 0.005158950067053849,(6, 20): 0.004684543328454343,(6, 21): 0.004151207772889528,(6, 22): 0.0036768010342900226,(6, 23): 0.003617276976749307}
        )
    )

    return weekly_weighted_disaggregate(
                                    monthly_demand=monthly_residential_load,
                                    weights=hourly_residential_profile,
                                )

from heatpro.temporal_demand import YearlyHeatDemand
from heatpro.disaggregation import monthly_weighted_disaggregate
from heatpro.demand_profile import month_length_proportionnal_weight, day_length_proportionnal_weight

@pytest.fixture
def hourly_industry_load(monthly_building_load,setup_data):
    parameters, external_factors = setup_data
    yearly_industry_load = YearlyHeatDemand(
                                                "industry",
                                                monthly_building_load.data.resample('YS').sum()*parameters["Part_Indu"]["fixed_perc"]
                                            )

    monthly_industry_load = monthly_weighted_disaggregate(
                                                                yearly_demand=yearly_industry_load,
                                                                weights = month_length_proportionnal_weight(pd.date_range('2021',end='2022',freq='MS',inclusive='left'))
                                                            )

    return weekly_weighted_disaggregate(
                                monthly_demand=monthly_industry_load,
                                weights=apply_weekly_hourly_pattern(
                                    hourly_index=external_factors.data.index,
                                    hourly_mapping={(day,hour): 1/24 for day in range(7) for hour in range(24)}
                                    )*\
                                    day_length_proportionnal_weight(dates=external_factors.data.index),
                            )
    
from heatpro.demand_profile import Y_to_H_thermal_loss_profile
from heatpro.temporal_demand import HourlyHeatDemand

@pytest.fixture
def hourly_heat_loss_load(monthly_building_load,induced_factors,setup_data):
    parameters = setup_data[0]
    yearly_heat_loss_load = YearlyHeatDemand(
                                                'heat_loss',
                                                monthly_building_load.data.resample('YE').sum()*parameters["Heat_Loss"]["fixed_perc"]
                                            )

    return HourlyHeatDemand(
                                            'heat_loss',
                                            (Y_to_H_thermal_loss_profile(induced_factors) * yearly_heat_loss_load.data[ENERGY_FEATURE_NAME].iloc[0]).rename(columns={'weight':ENERGY_FEATURE_NAME})
                                        )
    

from heatpro.district_heating_load import DistrictHeatingLoad
from heatpro.external_factors import RETURN_TEMPERATURE_NAME

@pytest.fixture
def district_heating(hourly_hot_water_load,hourly_industry_load,hourly_residential_load,hourly_heat_loss_load,induced_factors,setup_data):
    parameters, external_factors = setup_data
    district_heating = DistrictHeatingLoad(
                                demands = [
                                    hourly_hot_water_load,
                                    hourly_industry_load,
                                    hourly_residential_load,
                                    hourly_heat_loss_load,
                                ],
                                external_factors=external_factors,
                                district_network_temperature=induced_factors,
                                delta_temperature=parameters["Temp_DHN"]["Tret"]["dT_var"],
                                cp=parameters["Temp_ground"]["cp_ground"],
                            )

    district_heating.fit()
    return district_heating

def test_demands(district_heating):
    district_heating_reference = pd.read_csv("./tests/non_regression/data/district_heating.csv",index_col=0,parse_dates=True)
    for sector, hourly_load in district_heating.demands.items():
        absolute_gap = (hourly_load[ENERGY_FEATURE_NAME]-district_heating_reference[f"{sector}_{ENERGY_FEATURE_NAME}"]).abs()
        assert (absolute_gap <= EPSILON * district_heating_reference[f"{sector}_{ENERGY_FEATURE_NAME}"].abs()).all() , f"The relative gap of '{sector}' hourly demand is over {EPSILON}"

def test_return_temperature_after_fitting(district_heating):
    district_heating_reference = pd.read_csv("./tests/non_regression/data/district_heating.csv",index_col=0,parse_dates=True)
    absolute_gap = (district_heating.data[RETURN_TEMPERATURE_NAME] - district_heating_reference[RETURN_TEMPERATURE_NAME]).abs()
    assert (absolute_gap <= EPSILON * district_heating_reference[RETURN_TEMPERATURE_NAME].abs()).all() , f"The relative gap of return temperature after fitting is over {EPSILON}"

if __name__ == "__main__":
    district_heating_reference = pd.read_csv("./tests/non_regression/data/district_heating.csv",index_col=0,parse_dates=True)
    print(district_heating_reference.columns)
    