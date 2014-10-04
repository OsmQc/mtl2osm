ABBREVIATIONS = {
    'boul': 'boulevard',
    'aven': 'avenue',
    'stre': 'rue',
} 

def filterTags(attrs):
    if not attrs:
        return
    tags = {}
    if 'Name' in attrs:
      tags['name'] = attrs['Name']
    if 'description' in attrs:
      adresse, ville = attrs['description'].split('<br/>')[1:3]
      ville = ville.split('<')[0]
      tags['addr:housenumber'] = adresse.split()[0]
      tags['addr:street'] = adresse.split(' ', 1)[1]
      for abbr in ABBREVIATIONS:
        tags['addr:street'] = tags['addr:street'].replace(abbr, ABBREVIATIONS[abbr])
      tags['addr:city'] = ville
    return tags
