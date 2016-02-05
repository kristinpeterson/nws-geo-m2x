from nws_geo_m2x.db import DB

# FIPS6 county data obtained from: http://www.nws.noaa.gov/geodata/catalog/county/html/county.htm
fips_data_path_1 = 'data/fips1.csv'
fips_data_path_2 = 'data/fips2.csv'

# UGC data obtained from: http://www.nws.noaa.gov/geodata/catalog/wsom/html/cntyzone.htm
ugc_data_path = 'data/ugc.csv'

print "Initializing database with geo data"

def create_tables():
    try:
        print "Creating and populating FIPS table"
        db = DB()
        db.execute("DROP TABLE IF EXISTS fips;")
        db.execute("CREATE TABLE fips (geometry varchar, lat varchar, lon varchar, state varchar, cwa varchar, countyname varchar, fips varchar, time_zone varchar, fe_area varchar);")
        db.commit()
        populate_fips_table()
        print "FIPS table created and populated"
    except Exception as e:
        print "There was an error while creating the FIPS table"
        db.rollback()

    try:
        print "Creating and populating UGC table"
        db = DB()
        db.execute("DROP TABLE IF EXISTS ugc;")
        db.execute("CREATE TABLE ugc (state varchar, zone varchar, cwa varchar, name varchar, state_zone varchar, countyname varchar, fips varchar, time_zone varchar, fe_area varchar, lat varchar, lon varchar);")
        db.commit()
        populate_ugc_table()
        print "UGC table created and populated"
        print "Initialization script complete!"
    except Exception as e:
        print "There was an error while creating the UGC table"
        db.rollback()

def populate_fips_table():
    try:
        db = DB()
        db.copy_from(fips_data_path_1, 'fips', columns=('geometry', 'lat', 'lon', 'state', 'cwa', 'countyname', 'fips', 'time_zone', 'fe_area'), sep="|")
        db.commit()
        db.copy_from(fips_data_path_2, 'fips', columns=('geometry', 'lat', 'lon', 'state', 'cwa', 'countyname', 'fips', 'time_zone', 'fe_area'), sep="|")
        db.commit()
    except Exception as e:
        print e
        db.rollback()

def populate_ugc_table():
    try:
        db = DB()
        db.copy_from(ugc_data_path, 'ugc', columns=('state', 'zone', 'cwa', 'name', 'state_zone', 'countyname', 'fips', 'time_zone', 'fe_area', 'lat', 'lon'), sep="|")
        db.commit()
    except Exception as e:
        print e
        db.rollback()

create_tables()
