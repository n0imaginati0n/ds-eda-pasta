import json

def open_geojson(file_name):
    res = {}
    with open(file_name) as f:
        res = json.load(f)
    return res

def filter_zip_codes(geodata, zip_codes):
    features = [
        feat for feat in geodata['features'] if int(feat['properties']['ZCTA5CE10']) in zip_codes
    ]
    return features

def write_result_json(filename, geodata):
    with open(filename, 'w') as f:
        # f.write(json.dumps(geodata, indent=4))
        f.write(json.dumps(geodata))

if __name__ == '__main__':


    # df.zipcode.unique() gives a complete list of the interesting zip codes
    # let's make only these districts in view
    kings_county_zips = [
        98178, 98125, 98028, 98136, 98074, 98053, 98003, 98198, 98146,
        98038, 98007, 98115, 98107, 98126, 98019, 98103, 98002, 98133,
        98040, 98092, 98030, 98119, 98112, 98052, 98027, 98117, 98058,
        98001, 98056, 98166, 98023, 98070, 98148, 98105, 98042, 98008,
        98059, 98122, 98144, 98004, 98005, 98034, 98075, 98116, 98010,
        98118, 98199, 98032, 98045, 98102, 98077, 98108, 98168, 98177,
        98065, 98029, 98006, 98109, 98022, 98033, 98155, 98024, 98011,
        98031, 98106, 98072, 98188, 98014, 98055, 98039]
    
    washington_geojson = 'data/wa_washington_zip_codes_geo.min.json'
    seattle_geojson = 'data/seattle_zip_codes_geo.json'

    geodata = open_geojson(washington_geojson)
    blocks = filter_zip_codes(geodata, kings_county_zips)

    print(f"DC Washington has {len(geodata['features'])} districts, found {len(blocks)} of {len(kings_county_zips)}")

    geodata['features'] = blocks

    write_result_json(seattle_geojson, geodata)
