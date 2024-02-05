if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    print(f"Preprocessing: records with zero passengers: {data['passenger_count'].isin([0]).sum()}")
    print(f"Preprocessing: records with zero distant: {data['trip_distance'].isin([0]).sum()}")
    # print(type(data))
    filtered_data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]
    filtered_data['lpep_pickup_date'] = filtered_data['lpep_pickup_datetime'].dt.date
    filtered_data_coulmns = filtered_data.columns
    # print(filtered_data_coulmns)

    filtered_data.columns = (filtered_data.columns    
                            .str.replace('(?<=[a-z])(?=[A-Z])', '_', regex=True)
                            .str.lower()
    )
    filtered_data2 = filtered_data
    filtered_data2_columns = filtered_data2.columns
    # print(filtered_data2_columns)
    print(f'Number of columns to be renamed : {sum(filtered_data_coulmns != filtered_data2_columns)}')
    existing_vendor_ids = filtered_data['vendor_id'].unique().tolist()[:10]
    print("Existing values of VendorID:", existing_vendor_ids)

    return filtered_data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with zero passengers'
    assert output['trip_distance'].isin([0]).sum() == 0, 'There are rides with zero distant ride.'
    assert output['vendor_id'].isin([2,1]).all(), 'There is one of the existing values in the column (vendor_id)'
