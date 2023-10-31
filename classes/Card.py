import pygame, random, os

class Card:
  
  front = {
    "amexp": "aep",
    "birthday": "birthday",
    "business": "business",
    "atm": "credit",
    "flash": "flash",
    "pokemon": "game",
    "green": "green",
    "id": "id",
    "key": "key",
    "plac": "plac",
    "play": "playing",
    "post": "post",
    "uno": "reverse",
    "tarot": "tarot"
  }
  straps = {
    "none": None,
    "chain": "chain",
  }
  back = "back"

  prefixes = {
    "front": "assets/cards/front",
    "strap": "assets/cards/strap",
    "back": "assets/cards"
  }

  def __init__(self, _type:str, strap):
    self.location = None
    self.bounds = None
    self.properties = {
      "type": _type,
      "strap": strap,
      #"cursed": cursed,
      "flipped": False,
    }
    self.assets = self.get_assets(self.properties)

  def __repr__(self):
    return f"Card" # at {tuple(self.location)}"
  
  def get_assets(self, properties):
    return {
      "front": os.path.join(Card.prefixes["front"], Card.front[properties["type"]]),
      "back": os.path.join(Card.prefixes["back"], Card.back),
      "strap": os.path.join(Card.prefixes["strap"], Card.straps[properties["strap"]]) if properties["strap"] else None
    }
  
  def set_location(self, location:list):
    self.location = location

  def set_bounds(self, bounds:list):
    self.bounds = bounds

  def get_image(self, key):
    return f"{self.assets[key]}.png" if self.assets[key] else None

  def get_property(self, prop):
    return self.properties[prop]

  def set_property(self, prop, value):
    self.properties[prop] = value

  def update_assets(self):
    self.assets = self.get_assets(self.properties)

  def flip(self):
    self.set_property("flipped", not self.get_property("flipped"))

  def open(self):
    self.set_property("flipped", True)

  def close(self):
    self.set_property("flipped", False)