from dateutil import relativedelta
import analytics
import calendar
import datetime
import json
import random
import socket
import struct
import sys
import uuid

from_date = sys.argv[1]

#
# Add your Segment write keys here.
# You should have one source configured for web, ios, android, and email in
# your Segment workspace.
#

web_write_key = '8OjsXlxUPyxoCJONNG7AwFhPRH29zbMP'
android_write_key = 'nrLyVtRxcFCm27VB2oe91oYywgG5RzjA'
ios_write_key = 'wOMzkIO14oiRQjmdmG1YTJ5WChiNHmAo'
email_write_key = 'UOHMCZHtYL9C9TvXNkzyzXqcF9nEgiJo'
android_analytics = analytics.Client(android_write_key)
web_analytics = analytics.Client(web_write_key)
ios_analytics = analytics.Client(ios_write_key)
email_analytics = analytics.Client(email_write_key)
clients = [(android_analytics, 'Android'), (web_analytics, 'Web'), (ios_analytics, 'iOS')]
#clients = [(web_analytics, 'Web')]
custom_traits = [
  {'property_name': 'likelihood_to_buy', 'values': [(.50, 45), (.60, 40), (.40, 35), (.80, 32)]},
  {'property_name': 'lifetime_value', 'values': [(1000.00, 45), (2000.00, 40), (5000.00, 35), (400.00, 32)]}
]
registration_path = [
  {'event_name': 'Page Viewed', 'property_choices': {'page_name': [('Home', 20), ('Search', 55)]}},
  {'event_name': 'Signup Clicked', 'property_choices': {'page_name': [('Home', 20), ('Search', 40)]}},
  {'event_name': 'Signup Success', 'property_choices': {'page_name': [('Home', 20), ('Search', 40)]}}
]
usage_paths = [
  [
    {'event_name': 'Product Added',
      'property_choices': {
        'sku': [("adidas-classic-backpack", 5), ("adidas-classic-backpack-legend-ink-multicolour", 5), ("adidas-kids-stan-smith", 5), ("adidas-superstar-80s", 5), ("asics-tiger-gel-lyte-v-30-years-of-gel-pack", 5), ("black-leather-bag", 5), ("blue-silk-tuxedo", 5), ("chequered-red-shirt", 5), ("classic-leather-jacket", 5), ("classic-varsity-top", 5), ("converse-chuck-taylor-all-star-ii-hi", 5), ("converse-chuck-taylor-all-star-lo", 5), ("converse-toddler-chuck-taylor-all-star-axel-mid", 5), ("dark-denim-top", 5), ("dr-martens-1460z-dmc-8-eye-boot-cherry-smooth", 5), ("dr-martens-1461-dmc-3-eye-shoe-black-smooth", 5), ("dr-martens-cavendish-3-eye-shoe-black", 5), ("flex-fit-mini-ottoman-black", 5), ("floral-white-top", 5), ("herschel-iona", 5), ("led-high-tops", 5), ("longsleeve-cotton-top", 5), ("navy-sport-jacket", 5), ("nike-crackle-print-tb-tee", 5), ("nike-swoosh-pro-flat-peak-cap", 5), ("nike-toddler-roshe-one", 5), ("ocean-blue-shirt", 5), ("olive-green-jacket", 5), ("palladium-pallatech-hi-tx-chevron", 5), ("puma-suede-classic-regal", 5), ("red-sports-tee", 5), ("silk-summer-top", 5), ("dark-winter-jacket", 5), ("striped-silk-blouse", 5), ("striped-skirt-and-top", 5), ("supra-mens-vaider", 5), ("timberland-mens-6-inch-premium-boot", 5), ("vans-apparel-and-accessories-classic-super-no-show-socks-3-pack-white", 5), ("vans-era-59-moroccan-geo-dress-blues", 5), ("vans-authentic-butterfly-true-white-black", 5), ("vans-authentic-multi-eyelets-gradient-crimson", 5), ("vans-classic-slip-on-perforated-suede", 5), ("vans-era-59-desert-cowboy", 5), ("vans-old-skool-butterfly-true-white-black", 5), ("vans-sh-8-hi", 5), ("vans-sk8-hi-decon-cutout-leaves-white", 5), ("vans-authentic-lo-pro-burgandy-white", 5), ("white-cotton-shirt", 5), ("yellow-wool-jumper", 5), ("zipped-jacket", 5)]
      },
      'dependent_props_list': {
      }
    }
  ],
  [
    {'event_name': 'Product Clicked',
      'property_choices': {
        'sku': [("adidas-classic-backpack", 5), ("adidas-classic-backpack-legend-ink-multicolour", 5), ("adidas-kids-stan-smith", 5), ("adidas-superstar-80s", 5), ("asics-tiger-gel-lyte-v-30-years-of-gel-pack", 5), ("black-leather-bag", 5), ("blue-silk-tuxedo", 5), ("chequered-red-shirt", 5), ("classic-leather-jacket", 5), ("classic-varsity-top", 5), ("converse-chuck-taylor-all-star-ii-hi", 5), ("converse-chuck-taylor-all-star-lo", 5), ("converse-toddler-chuck-taylor-all-star-axel-mid", 5), ("dark-denim-top", 5), ("dr-martens-1460z-dmc-8-eye-boot-cherry-smooth", 5), ("dr-martens-1461-dmc-3-eye-shoe-black-smooth", 5), ("dr-martens-cavendish-3-eye-shoe-black", 5), ("flex-fit-mini-ottoman-black", 5), ("floral-white-top", 5), ("herschel-iona", 5), ("led-high-tops", 5), ("longsleeve-cotton-top", 5), ("navy-sport-jacket", 5), ("nike-crackle-print-tb-tee", 5), ("nike-swoosh-pro-flat-peak-cap", 5), ("nike-toddler-roshe-one", 5), ("ocean-blue-shirt", 5), ("olive-green-jacket", 5), ("palladium-pallatech-hi-tx-chevron", 5), ("puma-suede-classic-regal", 5), ("red-sports-tee", 5), ("silk-summer-top", 5), ("dark-winter-jacket", 5), ("striped-silk-blouse", 5), ("striped-skirt-and-top", 5), ("supra-mens-vaider", 5), ("timberland-mens-6-inch-premium-boot", 5), ("vans-apparel-and-accessories-classic-super-no-show-socks-3-pack-white", 5), ("vans-era-59-moroccan-geo-dress-blues", 5), ("vans-authentic-butterfly-true-white-black", 5), ("vans-authentic-multi-eyelets-gradient-crimson", 5), ("vans-classic-slip-on-perforated-suede", 5), ("vans-era-59-desert-cowboy", 5), ("vans-old-skool-butterfly-true-white-black", 5), ("vans-sh-8-hi", 5), ("vans-sk8-hi-decon-cutout-leaves-white", 5), ("vans-authentic-lo-pro-burgandy-white", 5), ("white-cotton-shirt", 5), ("yellow-wool-jumper", 5), ("zipped-jacket", 5)]
      },
      'dependent_props_list': {
      }
    }
  ]
]

email_spec = [
  {'event_name': 'Email Sent', 'property_choices': {
    'campaign_id': [(15203, 70), (22123, 55), (34321, 20), (41232, 55), (53213, 20), (61232, 55), (234321, 40), (923422, 50)],
    'app_id': [(15203, 70), (22123, 55), (34321, 20), (41232, 55), (53213, 20), (61232, 55), (234321, 40), (923422, 50)],
    'button_id': [(1, 70), (2, 55), (3, 20), (4, 55), (5, 20), (6, 55)],
  }},
  {'event_name': 'Email Delivered', 'property_choices': {
    'campaign_id': [(15203, 70), (22123, 55), (34321, 20), (41232, 55), (53213, 20), (61232, 55), (234321, 40), (923422, 50)],
    'app_id': [(15203, 70), (22123, 55), (34321, 20), (41232, 55), (53213, 20), (61232, 55), (234321, 40), (923422, 50)],
    'button_id': [(1, 70), (2, 55), (3, 20), (4, 55), (5, 20), (6, 55)],
  }},
  {'event_name': 'Email Opened', 'property_choices': {
    'campaign_id': [(15203, 70), (22123, 55), (34321, 20), (41232, 55), (53213, 20), (61232, 55), (234321, 40), (923422, 50)],
    'app_id': [(15203, 70), (22123, 55), (34321, 20), (41232, 55), (53213, 20), (61232, 55), (234321, 40), (923422, 50)],
    'button_id': [(1, 70), (2, 55), (3, 20), (4, 55), (5, 20), (6, 55)],
  }},
  {'event_name': 'Email Link Clicked', 'property_choices': {
    'campaign_id': [(15203, 70), (22123, 55), (34321, 20), (41232, 55), (53213, 20), (61232, 55), (234321, 40), (923422, 50)],
    'app_id': [(15203, 70), (22123, 55), (34321, 20), (41232, 55), (53213, 20), (61232, 55), (234321, 40), (923422, 50)],
    'button_id': [(1, 70), (2, 55), (3, 20), (4, 55), (5, 20), (6, 55)],
  }},
  {'event_name': 'Unsubscribe', 'property_choices': {
    'campaign_id': [(15203, 70), (22123, 55), (34321, 20), (41232, 55), (53213, 20), (61232, 55), (234321, 40), (923422, 50)],
    'app_id': [(15203, 70), (22123, 55), (34321, 20), (41232, 55), (53213, 20), (61232, 55), (234321, 40), (923422, 50)],
    'button_id': [(1, 70), (2, 55), (3, 20), (4, 55), (5, 20), (6, 55)],
  }},
]

def weighted_choice(choices):
  total = sum(w for c, w in choices)
  r = random.uniform(0, total)
  upto = 0
  for c, w in choices:
    if upto + w > r:
      return c
    upto += w

class User:
  def __init__(self, operating_system, custom_traits):
    self.anonymous_id = str(uuid.uuid4())
    self.user_id = random.randint(1000000000, 9999999999)
    self.traits = self.build_traits(operating_system, custom_traits)

  def build_traits(self, operating_system, custom_traits):
    traits = {}
    first_names = ['James','John','Robert','Michael','William','David','Richard','Charles','Joseph','Thomas','Christopher','Daniel','Paul','Mark','Donald','George','Kenneth','Steven','Edward','Brian','Ronald','Anthony','Kevin','Jason','Matthew','Gary','Timothy','Jose','Larry','Jeffrey','Frank','Scott','Eric','Stephen','Andrew','Raymond','Gregory','Joshua','Jerry','Dennis','Walter','Patrick','Peter','Harold','Douglas','Henry','Carl','Arthur','Ryan','Roger','Joe','Juan','Jack','Albert','Jonathan','Justin','Terry','Gerald','Keith','Samuel','Willie','Ralph','Lawrence','Nicholas','Roy','Benjamin','Bruce','Brandon','Adam','Harry','Fred','Wayne','Billy','Steve','Louis','Jeremy','Aaron','Randy','Howard','Eugene','Carlos','Russell','Bobby','Victor','Martin','Ernest','Phillip','Todd','Jesse','Craig','Alan','Shawn','Clarence','Sean','Philip','Chris','Johnny','Earl','Jimmy','Antonio','Danny','Bryan','Tony','Luis','Mike','Stanley','Leonard','Nathan','Dale','Manuel','Rodney','Curtis','Norman','Allen','Marvin','Vincent','Glenn','Jeffery','Travis','Jeff','Chad','Jacob','Lee','Melvin','Alfred','Kyle','Francis','Bradley','Jesus','Herbert','Frederick','Ray','Joel','Edwin','Don','Eddie','Ricky','Troy','Randall','Barry','Alexander','Bernard','Mario','Leroy','Francisco','Marcus','Micheal','Theodore','Mary','Patricia','Linda','Barbara','Elizabeth','Jennifer','Maria','Susan','Margaret','Dorothy','Lisa','Nancy','Karen','Betty','Helen','Sandra','Donna','Carol','Ruth','Sharon','Michelle','Laura','Sarah','Kimberly','Deborah','Jessica','Shirley','Cynthia','Angela','Melissa','Brenda','Amy','Anna','Rebecca','Virginia','Kathleen','Pamela','Martha','Debra','Amanda','Stephanie','Carolyn','Christine','Marie','Janet','Catherine','Frances','Ann','Joyce','Diane','Alice','Julie','Heather','Teresa','Doris','Gloria','Evelyn','Jean','Cheryl','Mildred','Katherine','Joan','Ashley','Judith','Rose','Janice','Kelly','Nicole','Judy','Christina','Kathy','Theresa','Beverly','Denise','Tammy','Irene','Jane','Lori','Rachel','Marilyn','Andrea','Kathryn','Louise','Sara','Anne','Jacqueline','Wanda','Bonnie','Julia','Ruby','Lois','Tina','Phyllis','Norma','Paula','Diana','Annie','Lillian','Emily','Robin','Peggy','Crystal','Gladys','Rita','Dawn','Connie','Florence','Tracy','Edna','Tiffany','Carmen','Rosa','Cindy','Grace','Wendy','Victoria','Edith','Kim','Sherry','Sylvia','Josephine']
    last_names = ['Smith','Johnson','Williams','Jones','Brown','Davis','Miller','Wilson','Moore','Taylor','Anderson','Thomas','Jackson','White','Harris','Martin','Thompson','Garcia','Martinez','Robinson','Clark','Rodriguez','Lewis','Lee','Walker','Hall','Allen','Young','Hernandez','King','Wright','Lopez','Hill','Scott','Green','Adams','Baker','Gonzalez','Nelson','Carter','Mitchell','Perez','Roberts','Turner','Phillips','Campbell','Parker','Evans','Edwards','Collins','Stewart','Sanchez','Morris','Rogers','Reed','Cook','Morgan','Bell','Murphy','Bailey','Rivera','Cooper','Richardson','Cox','Howard','Ward','Torres','Peterson','Gray','Ramirez','James','Watson','Brooks','Kelly','Sanders','Price','Bennett','Wood','Barnes','Ross','Henderson','Coleman','Jenkins','Perry','Powell','Long','Patterson','Hughes','Flores','Washington','Butler','Simmons','Foster','Gonzales','Bryant','Alexander','Russell','Griffin','Diaz','Hayes','Myers','Ford','Hamilton','Graham','Sullivan','Wallace','Woods','Cole','West','Jordan','Owens','Reynolds','Fisher','Ellis','Harrison','Gibson','Mcdonald','Cruz','Marshall','Ortiz','Gomez','Murray','Freeman','Wells','Webb','Simpson','Stevens','Tucker','Porter','Hunter','Hicks','Crawford','Henry','Boyd','Mason','Morales','Kennedy','Warren','Dixon','Ramos','Reyes','Burns','Gordon','Shaw','Holmes','Rice','Robertson','Hunt','Black','Daniels','Palmer','Mills','Nichols','Grant','Knight','Ferguson','Rose','Stone','Hawkins','Dunn','Perkins','Hudson','Spencer','Gardner','Stephens','Payne','Pierce','Berry','Matthews','Arnold','Wagner','Willis','Ray','Watkins','Olson','Carroll','Duncan','Snyder','Hart','Cunningham','Bradley','Lane','Andrews','Ruiz','Harper','Fox','Riley','Armstrong','Carpenter','Weaver','Greene','Lawrence','Elliott','Chavez','Sims','Austin','Peters','Kelley','Franklin','Lawson','Fields','Gutierrez','Ryan','Schmidt','Carr','Vasquez','Castillo','Wheeler','Chapman','Oliver','Montgomery','Richards','Williamson','Johnston','Banks','Meyer','Bishop','Mccoy','Howell','Alvarez','Morrison','Hansen','Fernandez','Garza','Harvey','Little','Burton','Stanley','Nguyen','George','Jacobs','Reid','Kim','Fuller','Lynch','Dean','Gilbert','Garrett','Romero','Welch','Larson','Frazier','Burke','Hanson','Day','Mendoza','Moreno','Bowman','Medina','Fowler','Brewer','Hoffman','Carlson','Silva','Pearson','Holland','Douglas','Fleming','Jensen','Vargas','Byrd','Davidson']
    email_domains = ['gmailx', 'yahoox', 'aolx', 'hotmailx']
    email_words = ['dragon','lancer','sword','fire','magic','dance','random','hacker','pike','trebuchet','catapult','iron','ranger','bow','arrow','strafe','hound','wiggle','darkness','light','coward','hero','giant','troll','dog','wolf','bear','puma','lion','pterodactyl','love','shadow','x']
    marketing_campaign_source = {'property_name': 'Campaign Source', 'values': [('Twitter', 20), ('Facebook', 55), ('Email', 12), ('Organic', 70), ('Google Adwords', 10)]}
    marketing_campaign_name = {'property_name': 'Campaign Name', 'values': [('Super Sale', 20), ('Buy Now', 15), ('Huge Discounts!', 25)]}
    invited_user = {'property_name': 'Invited User?', 'values': [('Invited User?', 10), ('Invited User?', 100)]}
    app_version = {'property_name': 'App Version', 'values': [('1.0.1', 5),('2.0.1', 10), ('3.0.1', 90)]}
    experiment_group = {'property_name': 'Experiment Group', 'values': [('Group A', 20), ('Group B', 20), ('Group C', 60)]}
    top_categories = {'property_name': 'Favorite Departments', 'values': [('Auto', 20), ('Accessories', 20), ('Clothing', 20), ('Beauty', 20), ('Electronics', 30)]}
    traits_to_add = [invited_user, experiment_group, marketing_campaign_source, top_categories]
    traits = self.modify_user(traits, traits_to_add)
    traits = self.modify_user(traits, custom_traits)
    iphone_models = {'property_name': 'model', 'values': [('iPhone4,1', 40) , ('iPhone3,1', 35), ('iPhone6,1', 50), ('iPhone5,2', 30), ('iPhone6,1', 45), ('iPhone5,1', 28), ('iPod5,1', 22), ('iPad2,5', 20), ('iPad3,4', 15), ('iPad4,1', 10)]}
    android_models = {'property_name': 'model', 'values': [('GT-I9300', 45), ('GT-I9500', 40), ('SM-G900F', 35), ('GT-I8190L', 32), ('XT1032', 28), ('Nexus 5', 25), ('LG-D802', 20)]}
    browser = {'property_name': 'browser', 'values': [('Chrome', 45), ('Firefox', 40), ('Safari', 35), ('Internet Explorer', 32)]}
    traits['operating_system'] = operating_system
    if traits['operating_system'] == 'iOS':
      self.modify_user(traits, [iphone_models, app_version])
    elif traits['operating_system'] == 'Android':
      self.modify_user(traits, [android_models, app_version])
    else:
      self.modify_user(traits, [browser])
    if traits['Campaign Source'] == 'Organic':
      traits['Campaign Name'] = 'Organic'
    else:
      self.modify_user(traits, [marketing_campaign_name])
    referrers = ['Organic', 'https://retailmenot.com','https://google.com','https://facebook.com','https://rxsaver.com']
    email = '%s.%s@%s.com' % (random.choice(email_words), random.choice(email_words), random.choice(email_domains))
    referrer = random.choice(referrers)
    traits.update({'first_name':random.choice(first_names), 'last_name':random.choice(last_names), 'email':email, 'Referrering Domain':referrer, 'ip': socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))})
    return traits

  def modify_user(self, traits, traits_to_add):
    for list_prop in traits_to_add:
      prop = weighted_choice(list_prop['values'])
      # if one value is organic, make all subsequent values organic
      if prop:
        traits.update({list_prop['property_name']:prop})
    return traits

  def get_user(self):
    return {'traits': self.traits, 'user_id': self.user_id, 'anonymous_id': self.anonymous_id}

def proceed(success_percent):
  if random.randint(1, 100) < success_percent:
    return True
  return False

def send_track(client, user, operating_system, event, timestamp):
  properties = build_event_properties(event, operating_system)
  client.track(user['user_id'], event['event_name'], properties, context={'ip': user['traits']['ip']}, anonymous_id=user['anonymous_id'], timestamp=datetime.datetime.fromtimestamp(timestamp))

def registration(registration_path, user_amount, timestamp, client, operating_system):
  for x in range(user_amount):
    user = User(operating_system, custom_traits).get_user()
    registration_funnel(client, user, operating_system, registration_path, 0, timestamp)

def registration_funnel(client, user, operating_system, registration_path, state, timestamp):
  timestamp = timestamp + random.randint(1,600)
  send_track(client, user, operating_system, registration_path[state], timestamp)
  success_percent = 50 + (state * 10)
  if proceed(success_percent):
    if len(registration_path) >= state + 2:
      registration_funnel(client, user, operating_system, registration_path, state + 1, timestamp)
    else:
      client.identify(user['user_id'], user['traits'], timestamp=datetime.datetime.fromtimestamp(timestamp))
      file = open('new_users.txt', 'a')
      file.write(json.dumps(user) + '\n')
      file.close()
      email_funnel(user, email_spec, operating_system, timestamp)
  return

def usage(usage_paths, operating_system, timestamp, client):
  try:
    users_file = open('registered_users.txt', 'r')
  except:
    users_file = []
  for user in users_file:
    user = json.loads(user)
    for path in usage_paths:
      usage_funnel(client, user, operating_system, path, timestamp, 0)
    if proceed(70):
      file = open('new_users.txt', 'a')
      file.write(json.dumps(user) + '\n')
      file.close()

def usage_funnel(client, user, operating_system, path, timestamp, state):
  if proceed(70 + (state * 10)):
    timestamp = timestamp + random.randint(1,600)
    send_track(client, user, operating_system, path[state], timestamp)
    if len(path) >= state + 2:
      usage_funnel(client, user, operating_system, path, timestamp, state + 1)
    elif proceed(10):
      usage_funnel(client, user, operating_system, path, timestamp, 0)
  return


def build_event_properties(event, operating_system):
  prop_choices = event['property_choices']
  properties = {}
  if event.get('dependent_props_list'):
    properties.update(assign_dependent_properties(event['dependent_props_list']))
  for prop_name in prop_choices:
    properties[prop_name] = weighted_choice(prop_choices[prop_name])
  properties.update(build_platform_properties(operating_system))
  return properties

def build_platform_properties(operating_system):
  properties = {'operating_system': operating_system}
  app_version = {'property_name': 'App Version', 'values': [('1.0.1', 5),('2.0.1', 10), ('3.0.1', 90)]}
  iphone_models = {'property_name': 'model', 'values': [('iPhone4,1', 40) , ('iPhone3,1', 35), ('iPhone6,1', 50), ('iPhone5,2', 30), ('iPhone6,1', 45), ('iPhone5,1', 28), ('iPod5,1', 22), ('iPad2,5', 20), ('iPad3,4', 15), ('iPad4,1', 10)]}
  android_models = {'property_name': 'model', 'values': [('GT-I9300', 45), ('GT-I9500', 40), ('SM-G900F', 35), ('GT-I8190L', 32), ('XT1032', 28), ('Nexus 5', 25), ('LG-D802', 20)]}
  browser = {'property_name': 'browser', 'values': [('Chrome', 45), ('Firefox', 40), ('Safari', 35), ('Internet Explorer', 32)]}
  if operating_system == 'Android':
    properties['app_version'] = weighted_choice(app_version['values'])
    properties['model'] = weighted_choice(android_models['values'])
  elif operating_system == 'iOS':
    properties['app_version'] = weighted_choice(app_version['values'])
    properties['model'] = weighted_choice(iphone_models['values'])
  elif operating_system == 'Web':
    properties['browser'] = weighted_choice(browser['values'])
  return properties


def assign_dependent_properties(prop_choices):
  properties = {}
  for prop_name in prop_choices:
    prop_value = weighted_choice(prop_choices[prop_name]['values'])
    properties[prop_name] = prop_value
    dependents = prop_choices[prop_name]['dependent_properties'][prop_value]
    for dependent in dependents:
      properties[dependent] = weighted_choice(dependents[dependent])
  return properties

def email_funnel(user, email_spec, operating_system, timestamp):
  for event in email_spec:
    timestamp += 400
    if proceed(70):
      send_track(email_analytics, user, operating_system, event, timestamp)
    else:
      return
  return

def stupid_file_switch(old_file, new_file):
  new = open(new_file, "r")
  old = open(old_file, "w")
  for user in new:
    old.write(user)
  old.close()
  new.close()
  new = open(new_file, "w")
  new.close()

def generate_data(registration_path, usage_paths, user_amount, from_date):
  from_date_list = from_date.split("-")
  from_date = datetime.date(int(from_date_list[0]), int(from_date_list[1]), int(from_date_list[2]))
  to_date = datetime.date.today()
  delta = (to_date - from_date).days
  for x in range(delta):
    request_date = str(from_date + relativedelta.relativedelta(days=x))
    #print request_date
    timestamp = calendar.timegm(datetime.datetime.strptime(request_date, "%Y-%m-%d").timetuple()) + 32400
    for client, operating_system in clients:
      registration(registration_path, user_amount, timestamp, client, operating_system)
      usage(usage_paths, operating_system, timestamp, client)
      stupid_file_switch('registered_users.txt', 'new_users.txt')
  for client, operating_system in clients:
    client.flush()

generate_data(registration_path, usage_paths, 1000, from_date)
