insert_query = 'insert into survey_system_survey values ' \
    	    '(%s, \'%s\', \'%s\', %s, %s, %s, \'%s\', \'%s\', \'%s\', \'%s\', %s, \'%s\');'

insert_listing = 'insert into listings_listing values ' \
			'(%s, %s, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', %s, \'%s\', \'%s\',' \
				'%s, \'%s\', \'%s\', \'%s\', \'%s\', %s, \'%s\', %s, \'%s\', \'%s\');'

date_time = '1111-11-11 11:11:11'
date_time_expired = '2222-11-11 11:11:11'

print 'DELETE FROM survey_system_survey;'
print 'DELETE FROM listings_listing;'

def shit(category, for_sale, start_id):
    for i in range(start_id, start_id+11):
        survey = insert_query % (i, i, category, i, i, i, 'street name', 'city', 
        	'postal', 'comments', i, date_time)
        listing = insert_listing % (i, int(for_sale), i, 'hubertngu@gmail.com', date_time, 
        	date_time, i, i, 1, category, i, i, 'street', 'city', 'postal', 
        	'location', 5, date_time_expired, 0, 'NULL', 
        	'47b54d20-8e78-11e2-9e96-0800200c9' + str(i))
        print survey
        print listing

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