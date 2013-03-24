CATEGORIES = ['Woods', 'Bricks', 'Shingles', 'Drywall', 'Toilets', 'Sinks',
                'Tubs', 'Windows', 'Doors', 'Fixtures', 'Cable and Wiring',
                'Particle board', 'Cardboard', 'Cabinetry', 'Scrap metal',
                'Appliances', 'Other']

insert_query = 'insert into survey_system_survey values (%s, %s, \'%s\', \'%s\', ' \
                '%s, \'%s\', \'%s\', \'%s\', \'%s\');'
insert_listing = 'insert into listings_listing values ' \
			'(%(id)s, \'%(for_sale)s\', \'%(url)s\', \'%(creator)s\', \'%(created)s\', \'%(last_modified)s\', ' \
                '\'%(title)s\', \'%(text_content)s\', %(verified)s, \'%(category)s\', ' \
                '\'%(price)s\', \'%(address)s\', \'%(city)s\', %(flag_count)s, ' \
                '\'%(expires)s\', %(expired)s, %(survey_time_sent)s, \'%(uuid)s\');'

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

        listing_mapping = dict()
        listing_mapping['id'] = START_ID
        listing_mapping['for_sale'] = for_sale
        listing_mapping['url'] = START_ID
        listing_mapping['creator'] = 'hubertngu@gmail.com'
        listing_mapping['created'] = date_time
        listing_mapping['last_modified'] = date_time
        listing_mapping['title'] = START_ID
        listing_mapping['text_content'] = START_ID
        listing_mapping['verified'] = 1
        listing_mapping['category'] = category
        listing_mapping['price'] = START_ID
        listing_mapping['address'] = '5141 Patrick Street'
        listing_mapping['city'] = 'Burnaby'
        listing_mapping['flag_count'] = 5
        listing_mapping['expires'] = date_time_expired
        listing_mapping['expired'] = 0
        listing_mapping['survey_time_sent'] = 'NULL'
        listing_mapping['uuid'] = uuid_id(UUID, START_ID)

        listing = insert_listing % listing_mapping
        START_ID = START_ID + 1
        print survey
        print listing
    globals()['START_ID'] = START_ID

for category in CATEGORIES:
    bebop(category, 'sell', 10)
    bebop(category, 'want', 10)