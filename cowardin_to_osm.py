import csv

class cowardin_decoder:
    def __init__(self, faws_filename = 'NWI_Code_Definitions.csv'):
        
        self.leaf_subclass_names = ['Broad-Leaved Deciduous', 'Needle-Leaved Deciduous', 'Broad-Leaved Evergreen', 'Needle-Leaved Evergreen', 'Deciduous', 'Evergreen']
        self.managed_modifiers = ['Partially Drained/Ditched', 'Diked/Impounded', 'Managed', 'Excavated', 'Artificial Substrate', 'Spoil']
        self.tidal_subgroups = ['Saltwater Tidal', 'Freshwater Tidal']
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
    
    def code_to_tags(self, code):
        attrs = self.code_defs[code]
        if attrs['SYSTEM_NAME'] == 'Palustrine':
            return self._palustrine_to_osm(attrs)


    def is_managed(self, attrs):
        '''
        Several modifiers corispond to the OSM tag managed=yes for wetlands
        '''
        return any([managed_modifier in attrs['MODIFIERS'] for managed_modifier in self.managed_modifiers])


    def parse_leaves(self, attrs):
        subclasses = [attrs['SUBCLASS_NAME'], attrs['SPLIT_SUBCLASS_NAME']]
        subclasses = ['Unspecified ' + subclass if len(subclass) < 10 else subclass for subclass in subclasses if subclass in self.leaf_subclass_names]

        leaf_types = [subclass.split()[0] for subclass in subclasses]
        leaf_cycles = [subclass.split()[1] for subclass in subclasses]

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

    def is_tidal(self, attrs):
        return attrs['WATER_REGIME_SUBGROUP'] in self.tidal_subgroups


    def _palustrine_to_osm(self, attrs):
        tags = []
        tags.append({'key':'natural', 'value':'wetland'})
        if self.is_tidal(attrs):
            tags.append({'key':'tidal', 'value':'yes'})
        if attrs['CLASS_NAME'] == 'Scrub-Shrub' or attrs['CLASS_NAME'] == 'Forested':
            tags.append({'key':'natural', 'value':'wetland'})
            tags.append({'key':'wetland','value':'swamp'})
            leaf_type, leaf_cycle = self.parse_leaves(attrs)
            if leaf_type != '':
                tags.append({'key':'leaf_type','value':leaf_type})
            if leaf_cycle != '':
                tags.append({'key':'leaf_cycle','value':leaf_cycle})
        elif attrs['CLASS_NAME'] == 'Moss-Lichen':
            tags.append({'key':'natural', 'value':'wetland'})
            tags.append({'key':'wetland','value':'bog'})
            #Should a Moss-Lichen class with high ph be a fen?
        elif attrs['CLASS_NAME'] == 'Emergent':
            tags.append({'key':'natural', 'value':'wetland'})
            if attrs['SUBCLASS_NAME'] == 'Phragmites australis':
                tags.append({'key':'wetland','value':'reedbed'})
            else:
                tags.append({'key':'wetland','value':'marsh'})
        return tags

