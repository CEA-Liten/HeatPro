import pandas as pd
import pytest
from heatpro.district_heating_load import DistrictHeatingLoad, ENERGY_FEATURE_NAME
from heatpro.temporal_demand import HourlyHeatDemand
from heatpro.external_factors import ExternalFactors, DEPARTURE_TEMPERATURE_NAME, RETURN_TEMPERATURE_NAME

# Sample data for testing
sample_demand_data = pd.DataFrame({
    ENERGY_FEATURE_NAME: [100, 150, 120, 180, 200],
        },index=pd.date_range('2022-01-01', periods=5, freq='h'))

sample_external_factors_data = pd.DataFrame({
    'external_temperature': [5, 6, 7, 8, 9],
    'heating_season': [0, 1, 1, 0, 0],
},index=pd.date_range('2022-01-01', periods=5, freq='h'))

sample_district_network_temperature_data = pd.DataFrame({
    'departure_temperature': [20, 18, 15, 16, 22],
    'return_temperature': [15, 14, 12, 11, 20],
},index=pd.date_range('2022-01-01', periods=5, freq='h'))

def test_district_heating_load_creation():
    demand = HourlyHeatDemand('SampleDemand', sample_demand_data)
    external_factors = ExternalFactors(sample_external_factors_data)
    district_network_temperature = sample_district_network_temperature_data
    delta_temperature = 5
    cp = 1.5

    district_heating_load = DistrictHeatingLoad([demand], external_factors, district_network_temperature, delta_temperature, cp)

    assert district_heating_load.demands == {'SampleDemand': sample_demand_data}
    assert district_heating_load.external_factors.data.equals(sample_external_factors_data)
    assert district_heating_load.district_network_temperature.equals(sample_district_network_temperature_data)
    assert district_heating_load.delta_temperature == 5
    assert district_heating_load.cp == 1.5

def test_district_heating_load_invalid_columns():
    demand = HourlyHeatDemand('SampleDemand', sample_demand_data)
    external_factors = ExternalFactors(sample_external_factors_data)
    invalid_district_network_temperature = pd.DataFrame({
        'invalid_column': [1, 2, 3, 4, 5],
    },index=pd.date_range('2022-01-01', periods=5, freq='h'))

    with pytest.raises(ValueError, match="district_network_temperature should have columns"):
        DistrictHeatingLoad([demand], external_factors, invalid_district_network_temperature, 5, 1.5)

def test_district_heating_load_index_mismatch():
    demand = HourlyHeatDemand('SampleDemand', sample_demand_data)
    external_factors = ExternalFactors(sample_external_factors_data)
    mismatched_district_network_temperature = pd.DataFrame({
        'departure_temperature': [20, 18, 15, 16, 22],
        'return_temperature': [15, 14, 12, 11, 20],
    },index=pd.date_range('2022-01-01', periods=5, freq='h'))

    mismatched_district_network_temperature.index += pd.Timedelta(hours=1)

    with pytest.raises(ValueError, match="Index between external_factors and district_network_temperature are not matching"):
        DistrictHeatingLoad([demand], external_factors, mismatched_district_network_temperature, 5, 1.5)

def test_district_heating_load_fit():
    demand = HourlyHeatDemand('SampleDemand', sample_demand_data)
    external_factors = ExternalFactors(sample_external_factors_data)
    district_network_temperature = sample_district_network_temperature_data
    delta_temperature = 5
    cp = 1.5

    district_heating_load = DistrictHeatingLoad([demand], external_factors, district_network_temperature, delta_temperature, cp)
    district_heating_load.fit()

    # Add more specific assertions based on the expected behavior of the fit method
