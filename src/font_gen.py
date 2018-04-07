import os
import random
import string
import copy
from fontTools.ttLib import TTFont


class FontGenerator(object):

    def __init__(self, base_font_path, char_map=None):
        """
        :base_font: The font to base the obsquired font on (file path)
        """
        font_ttf_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), base_font_path)

        self.base_font = TTFont(font_ttf_path)
        self.new_font = None
        if not char_map:
            self.character_map = self._generate_random_letter_map()
        else:
            self.character_map = char_map
        self.generate_font()

    def generate_font(self):
        assert self.base_font
        new_font = copy.deepcopy(self.base_font)
        original_cmap = self.base_font['cmap'].tables[0].cmap

        # remap characters
        for char_from, char_to in self.character_map.items():
            original_glyph = original_cmap[ord(char_from)]
            mapped_glyph = original_cmap[ord(char_to)]
            new_font.getGlyphSet()._glyphs.glyphs[original_glyph] = new_font.getGlyphSet()._glyphs.glyphs[mapped_glyph]

        # set name records
        new_font.get('name')  # this creates the table
        for nr in new_font.tables['name'].names:
            if nr.nameID == 0:
                nr.string = (nr.string.decode("ASCII")+" - REMAPPED").encode("ASCII")
        self.new_font = new_font

    def export_font(self, filename):
        if not self.new_font:
            raise Exception("Generate a font before exporting it")
        self.new_font.save(filename)

    def _generate_random_letter_map(self):
        """
        Generate a random map between characters
        [a-z,A-Z]
        """
        letters = string.ascii_letters + string.punctuation + " "
        shuffle_letters = random.sample(letters, k=len(letters))
        char_map = {}
        x = 0
        for a in shuffle_letters:
            char_map[a] = shuffle_letters[(x + 1) % len(letters)]
            x += 1
        return char_map

    def encode_string(self, string):
        new_string = []
        for char in string:
            new_char = [k for k, v in self.character_map.items() if v == char][0]
            new_string.append(new_char)
        return "".join(new_string)

    def decode_string(self, string):
        new_string = []
        for char in string:
            new_string.append(self.character_map[char])
        return "".join(new_string)
