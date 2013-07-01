#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sdl2.ext as sdl2ext
from sdl2 import pixels, render, events as sdlevents, surface, error
from sdl2.sdlttf import (TTF_OpenFont, 
						 TTF_RenderText_Shaded,
						 TTF_GetError,
						 TTF_Init,
						 TTF_Quit
						 )


class TextSprite(sdl2ext.TextureSprite):
	def __init__(self, renderer, fontPath, text = "", fontSize = 16, 
					   textColor = pixels.SDL_Color(255, 255, 255), 
					   backgroundColor = pixels.SDL_Color(0, 0, 0)):
		if isinstance(renderer, sdl2ext.RenderContext):
			self.renderer = renderer.renderer
		elif isinstance(renderer, render.SDL_Renderer):
			self.renderer = renderer
		else:
			raise TypeError("unsupported renderer type")
		
		self.font = TTF_OpenFont(fontPath, fontSize)
		self._text = text
		self.fontSize = fontSize
		self.textColor = textColor
		self.backgroundColor = backgroundColor
		texture = self._createTexture()
		
		super(TextSprite, self).__init__(texture)
	
	def _createTexture(self):
		textSurface = TTF_RenderText_Shaded(self.font, self._text, self.textColor, self.backgroundColor)
		if not textSurface:
			raise TTF_GetError()
		texture = render.SDL_CreateTextureFromSurface(self.renderer, textSurface)
		if not texture:
			raise sdl2ext.error.SDLError()
		surface.SDL_FreeSurface(textSurface)
		return texture
	
	@property
	def text(self):
		return self._text
	
	@text.setter
	def text(self, value):
		if self._text == value:
			return
		self._text = value
		super(TextSprite, self).__del__()
		texture = self._createTexture()
		super(TextSprite, self).__init__(texture)
		

class TextEntity(sdl2ext.Entity):
	def __init__(self, world, factory, fontPath, sprite):
		super(TextEntity, self).__init__(world)
		self.textSprite = sprite
	
	def changeText(self, value):
		self.textSprite.text = value

def main():
	sdl2ext.init()
	TTF_Init()
	RESSOURCE = sdl2ext.Resources(__file__, "resources")
	
	window = sdl2ext.Window("Text display", size=(800, 600))
	window.show()
	
	renderer = sdl2ext.RenderContext(window)
	factory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
	world = sdl2ext.World()
	
	fontPath = RESSOURCE.get_path("tuffy.ttf")
	textSprite = TextSprite(renderer, fontPath, "TEST")
	textEntity = TextEntity(world, renderer, fontPath, textSprite)
	spriteRenderer = sdl2ext.TextureSpriteRenderer(renderer)
	
	world.add_system(spriteRenderer)
	
	running = True
	
	textSprite.text = "Text is changed"
	
	while running:
		for event in sdl2ext.get_events():
			if event.type == sdlevents.SDL_QUIT:
				running = False
				break
		world.process()
	
	TTF_Quit()
	return 0

if __name__ == '__main__':
	
	main()

