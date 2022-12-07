import csv

class faws_decoder:
    def __init__(self, faws_filename = 'NWI_Code_Definitions.csv'):
        self.code_defs = {}
        with open(faws_filename, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',', quotechar="'")
            for row in csv_reader:
                code = row['ATTRIBUTE']
                self.code_defs[code] = row
                self.code_defs[code]['MODIFIERS'] = []
                if row['FIRST_MODIFIER_NAME'] != '':
                    self.code_defs[code]['MODIFIERS'].append(row['FIRST_MODIFIER_NAME'])
                if row['SECOND_MODIFIER_NAME'] != '':
                    self.code_defs[code]['MODIFIERS'].append(row['SECOND_MODIFIER_NAME'])
    
    def faws_to_osm(self, code):
        attrs = self.code_defs[code]

    def is_managed(self, attrs):
        '''
        Several modifiers corispond to the OSM tag managed=yes for wetlands
        '''
        managed_modifiers = ['Partially Drained/Ditched', 'Diked/Impounded', 'Managed', 'Excavated', 'Artificial Substrate', 'Spoil']
        return any([managed_modifier in attrs['MODIFIERS'] for managed_modifier in managed_modifiers])


    def parse_leaves(self, attrs):
        leaf_subclass_names = ['Broad-Leaved Deciduous', 'Needle-Leaved Deciduous', 'Broad-Leaved Evergreen', 'Needle-Leaved Evergreen', 'Deciduous', 'Evergreen']
        subclasses = [attrs['SUBCLASS_NAME'], attrs['SPLIT_SUBCLASS_NAME']]
        subclasses = ['Unspecified ' + subclass if len(subclass) < 10 else subclass for subclass in subclasses if subclass in leaf_subclass_names]

        leaf_types = [' '.split(subclass)[0] for subclass in subclasses]
        leaf_cycles = [' '.split(subclass)[1] for subclass in subclasses]

        def combine_leaf_types(type1, type2=None):
            type2 = type1 if type2 is None else type2
            if type1 == 'Unspecified' or type2 == 'Unspecified':
                return ''
            elif type1 == type2 == 'Needle-Leaved':
                return 'needleleaved'
            elif type1 == type2 == 'Broad-Leaved':
                return 'broadleaved'
            else:
                return 'mixed'
        def combine_leaf_cycles(type1, type2=None):
            type2 = type1 if type2 is None else type2
            if type1 == type2 == 'Deciduous':
                return 'deciduous'
            elif type1 == type2 == 'Evergreen':
                return 'evergreen'
            else:
                return 'mixed'
        
        return combine_leaf_types(*leaf_types), combine_leaf_cycles(*leaf_cycles)


    def _palustrine_to_osm(self, attrs):
        tags = []
        tags.append({'key':'natural', 'value':'wetland'})
        tidal = attrs['WATER_REGIME_SUBGROUP'] == 'Freshwater Tidal'

        if attrs['CLASS_NAME'] == 'Scrub-Shrub' or attrs['CLASS_NAME'] == 'Forested':
            tags.append({'key':'wetland','value':'swamp'})
            leaf_type, leaf_cycle = self.parse_leaves(attrs)
            if leaf_type != '':
                tags.append({'key':'leaf_type','value':leaf_type})
            if leaf_cycle != '':
                tags.append({'key':'leaf_cycle','value':leaf_cycle})
        elif attrs['CLASS_NAME'] == 'Moss-Lichen':
            tags.append({'key':'wetland','value':'bog'})
            #Should a Moss-Lichen class with high ph be a fen?
        elif attrs['CLASS_NAME'] == 'Emergent':
            if attrs['SUBCLASS_NAME'] == 'Phragmites australis':
                tags.append({'key':'wetland','value':'reedbed'})
            else:
                tags.append({'key':'wetland','value':'marsh'})

