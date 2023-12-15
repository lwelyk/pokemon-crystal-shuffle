#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate a .png of a metatileset from its tileset graphics, metatiles.bin, and
attributes.bin files.
"""

from __future__ import print_function

import sys
import os
import os.path
import re
import array

from itertools import izip_longest

import png

def chunk(L, n, fillvalue=None):
	return izip_longest(*[iter(L)] * n, fillvalue=fillvalue)

def rgb_bytes(rgbs):
	for px in rgbs:
		yield px[0]
		yield px[1]
		yield px[2]

default_rgb = (0xAB, 0xCD, 0xEF)

RGBC = lambda c: c * 8 # c * 33 // 4 for BGB instead of VBA
RGB5 = lambda r, g, b: (RGBC(r), RGBC(g), RGBC(b))

def load_palette(filename):
	try:
		palette = []
		with open(filename, 'r') as f:
			channels = []
			for line in f:
				line = line.split(';')[0].strip()
				if line.startswith('RGB '):
					rgbs = [RGBC(int(b)) for b in line[4:].split(',')]
					assert len(rgbs) % 3 == 0
					channels.extend(rgbs)
			hue = []
			while len(channels) >= 3:
				rgb, channels = channels[:3], channels[3:]
				hue.append(rgb)
				if len(hue) == 4:
					palette.append(hue)
					hue = []
	except:
		palette = [
			[RGB5(30,28,26), RGB5(19,19,19), RGB5(13,13,13), RGB5( 7, 7, 7)],
			[RGB5(30,28,26), RGB5(31,19,24), RGB5(30,10, 6), RGB5( 7, 7, 7)],
			[RGB5(18,24, 9), RGB5(15,20, 1), RGB5( 9,13, 0), RGB5( 7, 7, 7)],
			[RGB5(30,28,26), RGB5(15,16,31), RGB5( 9, 9,31), RGB5( 7, 7, 7)],
			[RGB5(30,28,26), RGB5(31,31, 7), RGB5(31,16, 1), RGB5( 7, 7, 7)],
			[RGB5(26,24,17), RGB5(21,17, 7), RGB5(16,13, 3), RGB5( 7, 7, 7)],
			[RGB5(30,28,26), RGB5(17,19,31), RGB5(14,16,31), RGB5( 7, 7, 7)],
			[RGB5(31,31,16), RGB5(31,31,16), RGB5(14, 9, 0), RGB5( 0, 0, 0)]
		]
	assert len(palette) >= 8
	return palette

class Tileset(object):
	WHITE, LIGHT, DARK, BLACK = range(4)

	p_per_t = 8

	def __init__(self, filename, attributes):
		self.attributes = attributes
		reader = png.Reader(filename=filename)
		self.w, self.h, data, metadata = reader.read_flat()
		self.wt, self.ht = self.w // Tileset.p_per_t, self.h // Tileset.p_per_t
		self.nt = self.wt * self.ht
		self.data = []

		if 'palette' in metadata:
			palette = metadata['palette']
			stride = 1
		else:
			palette = None
			stride = metadata['planes']
			if metadata['alpha']:
				stride += 1
		bitdepth = metadata['bitdepth']
		planes = metadata['planes']

		for i in range(self.w * self.h):
			px = data[i*stride:(i+1)*stride][0]
			if palette:
				px = palette[px][0]
			shade = 3 - 4 * px // (2 ** bitdepth)
			assert 0 <= shade < 4
			self.data.append(shade)

	def tile(self, i, attr):
		tile = []
		if attr & Attributes.BANK1:
			i |= 0x80
		else:
			i &= 0x7f
		ty, tx = divmod(i, self.wt)
		color = self.attributes.colors[attr & Attributes.COLOR]
		span = range(Tileset.p_per_t)
		if attr & Attributes.YFLIP:
			span = span[::-1]
		for r in span:
			start = ty*Tileset.p_per_t**2*self.wt + tx*Tileset.p_per_t + Tileset.p_per_t*self.wt*r
			row = self.data[start:start+Tileset.p_per_t]
			if attr & Attributes.XFLIP:
				row = row[::-1]
			row = [color[px] for px in row]
			tile.extend(row)
		if not tile:
			tile = [default_rgb] * Tileset.p_per_t**2
		return tile

	def tile_id_of_px(self, i):
		wt = self.wt
		tw = Tileset.p_per_t
		return (i // wt // (tw * tw) * wt) + (i // tw % wt)

class Attributes(object):
	GRAY, RED, GREEN, WATER, YELLOW, BROWN, ROOF, TEXT = range(8)
	COLOR    = 0x07
	BANK1    = 0x08
	XFLIP    = 0x20
	YFLIP    = 0x40
	PRIORITY = 0x80

	day_palette = staticmethod(lambda:
		(lambda x=load_palette('gfx/tilesets/bg_tiles.pal'): x[8:11]+[x[0x28]]+x[12:16])())
	nite_palette = staticmethod(lambda:
		(lambda x=load_palette('gfx/tilesets/bg_tiles.pal'): x[16:19]+[x[0x29]]+x[20:24])())
	indoor_palette = staticmethod(lambda:
		load_palette('gfx/tilesets/bg_tiles.pal')[32:40])

	map_palettes = {
  		'maps/OlivineCity.ablk': lambda: load_palette('utils/olivine.pal'),
  		'maps/Route38.ablk': lambda: load_palette('utils/olivine.pal'),
  		'maps/Route39.ablk': lambda: load_palette('utils/olivine.pal'),
  		'maps/MahoganyTown.ablk': lambda: load_palette('utils/mahogany.pal'),
  		'maps/Route42.ablk': lambda: load_palette('utils/mahogany.pal'),
  		'maps/Route44.ablk': lambda: load_palette('utils/mahogany.pal'),
  		'maps/EcruteakCity.ablk': lambda: load_palette('utils/ecruteak.pal'),
  		'maps/BlackthornCity.ablk': lambda: load_palette('utils/blackthorn.pal'),
  		'maps/Route45.ablk': lambda: load_palette('utils/blackthorn.pal'),
  		'maps/Route46.ablk': lambda: load_palette('utils/blackthorn.pal'),
  		'maps/CinnabarIsland.ablk': lambda: load_palette('utils/cinnabar.pal'),
  		'maps/Route19.ablk': lambda: load_palette('utils/cinnabar.pal'),
  		'maps/Route20.ablk': lambda: load_palette('utils/cinnabar.pal'),
  		'maps/Route21.ablk': lambda: load_palette('utils/cinnabar.pal'),
  		'maps/CeruleanCity.ablk': lambda: load_palette('utils/cerulean.pal'),
  		'maps/Route4.ablk': lambda: load_palette('utils/cerulean.pal'),
  		'maps/Route9.ablk': lambda: load_palette('utils/cerulean.pal'),
  		'maps/Route10North.ablk': lambda: load_palette('utils/cerulean.pal'),
  		'maps/Route24.ablk': lambda: load_palette('utils/cerulean.pal'),
  		'maps/Route25.ablk': lambda: load_palette('utils/cerulean.pal'),
  		'maps/AzaleaTown.ablk': lambda: load_palette('utils/azalea.pal'),
  		'maps/Route33.ablk': lambda: load_palette('utils/azalea.pal'),
  		'maps/LakeOfRage.ablk': lambda: load_palette('utils/lakeofrage.pal'),
  		'maps/Route43.ablk': lambda: load_palette('utils/lakeofrage.pal'),
  		'maps/VioletCity.ablk': lambda: load_palette('utils/violet.pal'),
  		'maps/Route32.ablk': lambda: load_palette('utils/violet.pal'),
  		'maps/Route35.ablk': lambda: load_palette('utils/violet.pal'),
  		'maps/Route36.ablk': lambda: load_palette('utils/violet.pal'),
  		'maps/Route37.ablk': lambda: load_palette('utils/violet.pal'),
  		'maps/GoldenrodCity.ablk': lambda: load_palette('utils/goldenrod.pal'),
  		'maps/Route34.ablk': lambda: load_palette('utils/goldenrod.pal'),
  		'maps/VermillionCity.ablk': lambda: load_palette('utils/vermillion.pal'),
  		'maps/Route6.ablk': lambda: load_palette('utils/vermillion.pal'),
  		'maps/Route11.ablk': lambda: load_palette('utils/vermillion.pal'),
  		'maps/PalletTown.ablk': lambda: load_palette('utils/pallet.pal'),
  		'maps/Route1.ablk': lambda: load_palette('utils/pallet.pal'),
  		'maps/PewterCity.ablk': lambda: load_palette('utils/pewter.pal'),
  		'maps/Route3.ablk': lambda: load_palette('utils/pewter.pal'),
  		'maps/MountMoonSquare.ablk': lambda: load_palette('utils/mountmoonsquare.pal'),
  		'maps/Route23.ablk': lambda: load_palette('utils/indigo.pal'),
  		'maps/FuchsiaCity.ablk': lambda: load_palette('utils/fuchsia.pal'),
  		'maps/Route13.ablk': lambda: load_palette('utils/fuchsia.pal'),
  		'maps/Route14.ablk': lambda: load_palette('utils/fuchsia.pal'),
  		'maps/Route15.ablk': lambda: load_palette('utils/fuchsia.pal'),
  		'maps/Route18.ablk': lambda: load_palette('utils/fuchsia.pal'),
  		'maps/LavenderTown.ablk': lambda: load_palette('utils/lavender.pal'),
  		'maps/Route8.ablk': lambda: load_palette('utils/lavender.pal'),
  		'maps/Route12.ablk': lambda: load_palette('utils/lavender.pal'),
  		'maps/Route10South.ablk': lambda: load_palette('utils/lavender.pal'),
  		'maps/Route28.ablk': lambda: load_palette('utils/silvercave.pal'),
  		'maps/CeladonCity.ablk': lambda: load_palette('utils/celadon.pal'),
  		'maps/Route7.ablk': lambda: load_palette('utils/celadon.pal'),
  		'maps/Route16.ablk': lambda: load_palette('utils/celadon.pal'),
  		'maps/Route17.ablk': lambda: load_palette('utils/celadon.pal'),
  		'maps/Route40.ablk': lambda: load_palette('utils/cianwood.pal'),
  		'maps/Route41.ablk': lambda: load_palette('utils/cianwood.pal'),
  		'maps/CianwoodCity.ablk': lambda: load_palette('utils/cianwood.pal'),
  		'maps/ViridianCity.ablk': lambda: load_palette('utils/viridian.pal'),
  		'maps/Route2.ablk': lambda: load_palette('utils/viridian.pal'),
  		'maps/Route22.ablk': lambda: load_palette('utils/viridian.pal'),
  		'maps/NewBarkTown.ablk': lambda: load_palette('utils/newbark.pal'),
  		'maps/Route26.ablk': lambda: load_palette('utils/newbark.pal'),
  		'maps/Route27.ablk': lambda: load_palette('utils/newbark.pal'),
  		'maps/Route29.ablk': lambda: load_palette('utils/newbark.pal'),
  		'maps/SaffronCity.ablk': lambda: load_palette('utils/saffron.pal'),
  		'maps/Route5.ablk': lambda: load_palette('utils/saffron.pal'),
  		'maps/CherrygroveCity.ablk': lambda: load_palette('utils/cherrygrove.pal'),
  		'maps/Route30.ablk': lambda: load_palette('utils/cherrygrove.pal'),
  		'maps/Route31.ablk': lambda: load_palette('utils/cherrygrove.pal'),
  		'maps/BattleTowerOutside.ablk': lambda: load_palette('utils/cianwood.pal'),
	}

	tileset_palettes = {
		'johto': lambda: Attributes.day_palette(),
		'johto_modern': lambda: Attributes.day_palette(),
		'kanto': lambda: Attributes.day_palette(),
		'battle_tower_outside': lambda: Attributes.day_palette(),
		'house': lambda: load_palette('gfx/tilesets/house.pal'),
		'players_house': lambda: Attributes.day_palette(),
		'pokecenter': lambda: Attributes.day_palette(),
		'gate': lambda: Attributes.day_palette(),
		'port': lambda: Attributes.day_palette(),
		'lab': lambda: Attributes.day_palette(),
		'facility': lambda: Attributes.day_palette(),
		'mart': lambda: Attributes.day_palette(),
		'mansion': lambda: load_palette('gfx/tilesets/mansion_1.pal'),
		'game_corner': lambda: Attributes.day_palette(),
		'elite_four_room': lambda: Attributes.day_palette(),
		'traditional_house': lambda: load_palette('gfx/tilesets/house.pal'),
		'train_station': lambda: Attributes.day_palette(),
		'champions_room': lambda: Attributes.day_palette(),
		'lighthouse': lambda: Attributes.day_palette(),
		'players_room': lambda: Attributes.day_palette(),
		'pokecom_enter': lambda: load_palette('gfx/tilesets/pokecom_center.pal'),
		'battle_tower_inside': lambda: load_palette('gfx/tilesets/battle_tower_inside.pal'),
		'tower': lambda: Attributes.day_palette(),
		'cave': lambda: Attributes.nite_palette(),
		'park': lambda: Attributes.day_palette(),
		'ruins_of_alph': lambda: Attributes.day_palette(),
		'radio_tower': lambda: load_palette('gfx/tilesets/radio_tower.pal'),
		'underground': lambda: Attributes.day_palette(),
		'ice_path': lambda: load_palette('gfx/tilesets/ice_path.pal'),
		'dark_cave': lambda: Attributes.nite_palette(),
		'forest': lambda: Attributes.nite_palette(),
		'beta_word_room': lambda: Attributes.day_palette(),
		'ho_oh_word_room': lambda: Attributes.day_palette(),
		'kabuto_word_room': lambda: Attributes.day_palette(),
		'omanyte_word_room': lambda: Attributes.day_palette(),
		'aerodactyl_word_room': lambda: Attributes.day_palette(),
	}

	def __init__(self, filename, key, map_blk):
		colors_lambda = Attributes.map_palettes.get(map_blk,
			Attributes.tileset_palettes.get(key, Attributes.day_palette))
		self.colors = colors_lambda()
		assert len(self.colors) == 8
		self.data = []
		with open(filename, 'rb') as file:
			while True:
				tile_attrs = [ord(c) for c in file.read(Metatiles.t_per_m**2)]
				if not len(tile_attrs):
					break
				self.data.append(tile_attrs)

	def color4(self, i):
		return self.colors[self.data[i]] if i < len(self.data) else [default_rgb] * 4

class Metatiles(object):
	t_per_m = 4

	def __init__(self, filename, tileset, attributes):
		self.tileset = tileset
		self.attributes = attributes
		self.data = []
		with open(filename, 'rb') as file:
			i = 0
			while True:
				tile_indexes = [ord(c) for c in file.read(Metatiles.t_per_m**2)]
				if not len(tile_indexes):
					break
				attr_indexes = self.attributes.data[i]
				metatile = [tileset.tile(ti, ta) for ti, ta in zip(tile_indexes, attr_indexes)]
				self.data.append(metatile)
				i += 1

	def size(self):
		return len(self.data)

	def export_colored(self, filename):
		wm = 4
		hm = self.size() // wm
		if wm * hm < self.size():
			hm += 1
		overall_w = wm * Metatiles.t_per_m * Tileset.p_per_t
		overall_h = hm * Metatiles.t_per_m * Tileset.p_per_t
		data = [default_rgb] * (overall_w * overall_h)

		for d_i in range(overall_w * overall_h):
			d_y, d_x = divmod(d_i, wm * Metatiles.t_per_m * Tileset.p_per_t)
			m_x, r_x = divmod(d_x, Metatiles.t_per_m * Tileset.p_per_t)
			t_x, p_x = divmod(r_x, Tileset.p_per_t)
			m_y, r_y = divmod(d_y, Metatiles.t_per_m * Tileset.p_per_t)
			t_y, p_y = divmod(r_y, Tileset.p_per_t)
			m_i = m_y * wm + m_x
			t_i = t_y * Metatiles.t_per_m + t_x
			p_i = p_y * Tileset.p_per_t + p_x
			if m_i >= self.size():
				continue
			metatile = self.data[m_i]
			tile = metatile[t_i]
			pixel = tile[p_i]
			data[d_i] = pixel

		with open(filename, 'wb') as file:
			writer = png.Writer(overall_w, overall_h)
			writer.write(file, chunk(rgb_bytes(data), overall_w * 3))

def process(key, tileset_name, metatiles_name, attributes_name, map_blk):
	attributes = Attributes(attributes_name, key, map_blk)
	tileset = Tileset(tileset_name, attributes)
	metatiles = Metatiles(metatiles_name, tileset, attributes)

	metatiles_colored_name = metatiles_name[:-4] + '.png'
	metatiles.export_colored(metatiles_colored_name)
	print('Exported', metatiles_colored_name)

def main():
	valid = False
	if len(sys.argv) in [2, 3]:
		name = sys.argv[1]
		tileset = 'gfx/tilesets/%s.2bpp.lz' % name
		metatiles = 'data/tilesets/%s_metatiles.bin' % name
		attributes = 'data/tilesets/%s_attributes.bin' % name
		map_blk = sys.argv[2] if len(sys.argv) == 3 else None
	elif len(sys.argv) in [4, 5]:
		name = None
		tileset = sys.argv[1]
		metatiles = sys.argv[2]
		attributes = sys.argv[3]
		map_blk = sys.argv[4] if len(sys.argv) == 5 else None
	else:
		usage = '''Usage: %s tileset [metatiles.bin attributes.bin map.blk]
       Generate a .png of a metatileset for viewing

       If tileset is gfx/tilesets/FOO.{2bpp.lz,2bpp,png},
       the other parameters will be inferred as
       data/tilesets/FOO_metatiles.bin and data/tilesets/FOO_attributes.bin.

       If tileset is FOO, it will first be inferred as
       gfx/tilesets/FOO.2bpp.lz.

       If a map is specified, its unique palette may be used.'''
		print(usage % sys.argv[0], file=sys.stderr)
		sys.exit(1)

	if tileset.endswith('.2bpp.lz') and not os.path.exists(tileset):
		tileset = tileset[:-3]

	if not tileset.endswith('.png'):
		os.system('python utils/gfx.py png %s' % tileset)
	if tileset.endswith('.2bpp'):
		tileset = tileset[:-5] + '.png'
	elif tileset.endswith('.2bpp.lz'):
		tileset = tileset[:-8] + '.png'

	process(name, tileset, metatiles, attributes, map_blk)

if __name__ == '__main__':
	main()
