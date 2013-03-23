CATEGORIES = ['Woods', 'Bricks', 'Shingles', 'Drywall', 'Toilets', 'Sinks',
                'Tubs', 'Windows', 'Doors', 'Fixtures', 'Cable and Wiring',
                'Particle board', 'Cardboard', 'Cabinetry', 'Scrap metal',
                'Appliances', 'Other']

insert_query = 'insert into survey_system_survey values (%s, %s, \'%s\', \'%s\', ' \
                '%s, \'%s\', \'%s\', \'%s\', \'%s\');'
insert_listing = 'insert into listings_listing values ' \
			'(%s, %s, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', %s, \'%s\', \'%s\',' \
				'%s, \'%s\', \'%s\', \'%s\', \'%s\', %s, \'%s\', %s, \'%s\', \'%s\');'

START_ID = 1

UUID = '1bbd94b0-9342-11e2-9e96-0800200c9a66'
date_time = '1111-11-11 11:11:11'
date_time_expired = '2222-11-11 11:11:11'

print 'DELETE FROM survey_system_survey;'
print 'DELETE FROM listings_listing;'

def uuid_id(uuid, id):
    return uuid[:len(uuid) - len(str(id))] + str(id)

def bebop(category, for_sale, records):
    START_ID = globals()['START_ID']
    for _ in range(records):
        survey = insert_query % (START_ID, START_ID, 'item' + str(START_ID), category, 
            START_ID, 'address' + str(START_ID), 
            'city' + str(START_ID), 'comments' + str(START_ID), date_time)
        listing = insert_listing % (START_ID, for_sale, START_ID, 
            'hubertngu@gmail.com', date_time, date_time, START_ID, 
            START_ID, 1, category, START_ID, START_ID, 'street' + str(START_ID), 
            'city' + str(START_ID), 'postal' + str(START_ID), 
            'location' + str(START_ID), 5, date_time_expired, 0, 'NULL', 
            uuid_id(UUID, START_ID))
        START_ID = START_ID + 1
        print survey
        print listing
    globals()['START_ID'] = START_ID

for category in CATEGORIES:
    bebop(category, 0, 1)
    bebop(category, 1, 1)

# 17 * 10 * 2 = 340
# 17 * 100 * 2 = 3400
# 34000

'''
def shit(category, for_sale, start_id):
    for i in range(start_id, start_id+90):
        survey = insert_query % (i, i, category, i, i, i, 'street name', 'city', 
        	'postal', 'comments', i, date_time)
        listing = insert_listing % (i, int(for_sale), i, 'hubertngu@gmail.com', date_time, 
        	date_time, i, i, 1, category, i, i, 'street', 'city', 'postal', 
        	'location', 5, date_time_expired, 0, 'NULL', 
        	'47b54d20-8e78-11e2-9e96-0800200c9' + str(i))
        #print survey
        #print listing

shit('Woods', 0, 100)
shit('Bricks', 0, 200)
shit('Shingles', 0, 300)
shit('Drywall', 0, 400)
shit('Toilets', 0, 500)
shit('Sinks', 0, 600)
shit('Tubs', 0, 700)
shit('Windows', 0, 800)
shit('Doors', 0, 900)
shit('Fixtures', 0, 1100)
shit('Cable and Wiring', 0, 2100)
shit('Particle board', 0, 3100)
shit('Cardboard', 0, 4100)
shit('Cabinetry', 0, 5100)
shit('Scrap metal', 0, 6100)
shit('Appliances', 0, 7100)
    
shit('Woods', 1, 9100)
shit('Bricks', 1, 9200)
shit('Shingles', 1, 9300)
shit('Drywall', 1, 9400)
shit('Toilets', 1, 9500)
shit('Sinks', 1, 9600)
shit('Tubs', 1, 9700)
shit('Windows', 1, 9800)
shit('Doors', 1, 9900)
shit('Fixtures', 1, 91100)
shit('Cable and Wiring', 1, 92100)
shit('Particle board', 1, 93100)
shit('Cardboard', 1, 94100)
shit('Cabinetry', 1, 95100)
shit('Scrap metal', 1, 96100)
shit('Appliances', 1, 97100)
'''
