#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sdl2.ext as sdl2ext
from sdl2 import pixels, render, events as sdlevents, surface
from sdl2.sdlttf import (TTF_OpenFont, 
						 TTF_RenderText_Shaded,
						 TTF_GetError,
						 TTF_Init,
						 TTF_Quit
						 )


class TextSprite(sdl2ext.TextureSprite):
	def __init__(self, spriteFactory, fontPath, text = "", fontSize = 16, 
					   textColor = pixels.SDL_Color(255, 255, 255), 
					   backgroundColor = pixels.SDL_Color(0, 0, 0)):
		self.spriteFactory = spriteFactory
		self.font = TTF_OpenFont(fontPath, fontSize)
		self.text = text
		self.fontSize = fontSize
		self.textColor = textColor
		self.backgroundColor = backgroundColor
		textSurface = TTF_RenderText_Shaded(self.font, text, textColor, backgroundColor)
		if not textSurface:
			raise TTF_GetError()
		self.sprite = self.spriteFactory.from_surface(textSurface, free=True)
		super(TextSprite, self).__init__(self.sprite.texture)

class TextEntity(sdl2ext.Entity):
	def __init__(self, world, factory, fontPath):
		super(TextEntity, self).__init__(world)
		self.textSprite = TextSprite(factory, fontPath, "TEST")

def main():
	sdl2ext.init()
	TTF_Init()
	RESSOURCE = sdl2ext.Resources(__file__, "resources")
	
	window = sdl2ext.Window("Text display", size=(800, 600))
	window.show()
	
	renderer = sdl2ext.RenderContext(window)
	factory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
	world = sdl2ext.World()
	
	textEntity = TextEntity(world, factory, RESSOURCE.get_path("tuffy.ttf"))
	spriteRenderer = sdl2ext.TextureSpriteRenderer(renderer)
	
	world.add_system(spriteRenderer)
	
	running = True
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

