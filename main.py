import pygame, random, copy, sys
from classes.Card import Card

pygame.init()
def_win_size = (700, 500)

window = pygame.display.set_mode(def_win_size)
clock = pygame.time.Clock()

icon = pygame.image.load("assets/icon.png").convert()
pygame.display.set_icon(icon)

FPS = 60

CARD_LIST = [
  "amexp",
  "birthday",
  "business",
  "atm",
  "flash",
  "pokemon",
  "green",
  "id",
  "key",
  "plac",
  "play",
  "post",
  "uno",
  "tarot"
]

STRAP_LIST = [
  None,
  "chain",
]

DECK_SIZE = (7, 4)

def draw_menu_window(frame):
  frame_set = frame//40%4

  title_logo = pygame.image.load("assets/ui/title_logo.png").convert_alpha()
  title_logo = pygame.transform.scale_by(title_logo, 3)

  window.blit(
    title_logo,
    (
      pygame.display.get_window_size()[0]//2 - title_logo.get_width()//2,
      140
    )
  )

  if frame <= 120:
    text_str = "Made by Dominic <3"
  elif 120 < frame < 180:
    text_str = "Made by Dominic <3"[:-(int(((frame - 120)/60) * (18 - 1)) + 1)]
  elif 180 <= frame < 240:
    text_str = "Click anywhere to start"[:(int(((frame - 180)/60) * (23 - 1)) + 1)]
  else:
    text_str = "Click anywhere to start" + "."*frame_set

  text = get_text_image("subtitle", text_str)
  text = pygame.transform.scale_by(text, 2)
  text.set_colorkey(0)

  window.blit(
    text,
    (
      pygame.display.get_window_size()[0]//2 - text.get_width()//2,
      310
    )
  )

def draw_win_window(guesses):
  trophy = pygame.image.load("assets/ui/win_trophy.png").convert_alpha()
  trophy = pygame.transform.scale_by(trophy, 3)

  window.blit(
    trophy,
    (
      pygame.display.get_window_size()[0]//2 - trophy.get_width()//2,
      140
    )
  )

  guess_str = get_text_image("subtitle", f"You completed the game in {guesses} guesses!")
  guess_str = pygame.transform.scale_by(guess_str, 2)
  guess_str.set_colorkey(0)

  restart_str = get_text_image("subtitle", f"[R] Restart")
  restart_str = pygame.transform.scale_by(restart_str, 1.5)
  restart_str.set_colorkey(0)

  exit_str = get_text_image("subtitle", f"[ESC] Exit Game")
  exit_str = pygame.transform.scale_by(exit_str, 1.5)
  exit_str.set_colorkey(0)

  window.blit(
    guess_str,
    (
      pygame.display.get_window_size()[0]//2 - guess_str.get_width()//2,
      310
    )
  )

  window.blit(
    restart_str,
    (
      pygame.display.get_window_size()[0]//2 - restart_str.get_width()//2,
      400
    )
  )

  window.blit(
    exit_str,
    (
      pygame.display.get_window_size()[0]//2 - exit_str.get_width()//2,
      420
    )
  )

def generate_cards(deck_size):
  deck = [i for i in range(deck_size[0] * deck_size[1])]
  card_types = copy.deepcopy(CARD_LIST)

  for i in range(0, len(deck), 2):
    card_type = card_types.pop(random.randint(0, len(card_types) - 1))
    
    strap_1 = random.choices(
      STRAP_LIST, weights=[0.75]+[0.25/(len(STRAP_LIST)-1) for i in range(1, len(STRAP_LIST))]
    )[0] # get strap of card1
    strap_2 = random.choices(
      STRAP_LIST, weights=[0.75]+[0.25/(len(STRAP_LIST)-1) for i in range(1, len(STRAP_LIST))]
    )[0] if not strap_1 else None # get strap of card2 if card1 has no strap

    deck[i] = Card(card_type, strap_1)
    deck[i+1] = Card(card_type, strap_2)

  return shuffle_deck(deck, deck_size)

def shuffle_deck(deck, deck_size):
  random.shuffle(deck) # shuffle cards
  deck = [deck[deck_size[1]*i:deck_size[1]*(i+1)] for i in range(len(deck)//deck_size[1])] # 1d list to 2d list

  for x, i in enumerate(deck):
    for y, card in enumerate(i):
      card.set_location([x, y]) # set location of card

  return deck

def draw_playing_window(deck, deck_size, guesses):

  # defining the board
  board_padding = (25, 35, 25, 65)
  board = pygame.Surface(
    (
      pygame.display.get_window_size()[0] - board_padding[0] - board_padding[2],
      pygame.display.get_window_size()[1] - board_padding[1] - board_padding[3]
    )
  )

  # retreiving size of card containers
  card_container_size = (
    board.get_size()[0]/deck_size[0], board.get_size()[1]/deck_size[1]
  )

  # defining every single card container & its contents
  for x, col in enumerate(deck):
    for y, card in enumerate(col):
      card_container = pygame.Surface(card_container_size)
      
      card_padding = (10, 5)
      card_image = pygame.image.load(card.get_image("front" if card.get_property("flipped") == True else "back")).convert_alpha()
      strap_image = pygame.image.load(card.get_image("strap")).convert_alpha() if card.get_property("strap") != None else None

      scale = (
          (card_container_size[1] - 2 * card_padding[0]) / card_image.get_height(),
          (card_container_size[0] - 2 * card_padding[1]) / card_image.get_width()
        ) # set scales on different axes
      scale = min(*scale) # set most fitting scale

      card_image = pygame.transform.scale_by(card_image, scale) # scale card image
      if strap_image != None:
        strap_image = pygame.transform.scale_by(strap_image, scale) # scale strap image if applicable

      card_container.blit(card_image, (
        card_container_size[0]/2 - card_image.get_size()[0]/2,
        card_container_size[1]/2 - card_image.get_size()[1]/2
      )) # blitting the card image
      if strap_image != None and card.get_property("flipped"):
        card_container.blit(strap_image, (
          card_container_size[0]/2 - card_image.get_size()[0]/2,
          card_container_size[1]/2 - card_image.get_size()[1]/2
        )) #blitting the strap image if applicable

      board.blit(card_container, (
        card_container_size[0] * x, card_container_size[1] * y
      )) # blitting the card container

      card.set_bounds(
        ((
          int(board_padding[0] + card_container_size[0] * x + (card_container_size[0]/2 - card_image.get_size()[0]/2)),
          int(board_padding[1] + card_container_size[1] * y + (card_container_size[1]/2 - card_image.get_size()[1]/2))
        ),
        (
          int(board_padding[0] + card_container_size[0] * x + (card_container_size[0]/2 - card_image.get_size()[0]/2) + card_image.get_size()[0]),
          int(board_padding[1] + card_container_size[1] * y + (card_container_size[1]/2 - card_image.get_size()[1]/2) + card_image.get_size()[1])
        ))
      ) # set physical location of card

  # blitting the board
  window.blit(board, (board_padding[0], board_padding[1]))

  bottom_bar = pygame.image.load("assets/ui/bottom.png")
  bottom_bar = pygame.transform.scale_by(
    bottom_bar, pygame.display.get_window_size()[0] // bottom_bar.get_width()
  )
  window.blit(bottom_bar, (0, pygame.display.get_window_size()[1] - bottom_bar.get_height()))
  
  guess_img = get_text_image("main", f"{guesses}").convert()
  guess_img.set_colorkey(0x000000)
  guess_padding = (15, 0, 5, 0)
  guess_img = pygame.transform.scale_by(
    guess_img, (bottom_bar.get_height() - guess_padding[0] - guess_padding[2]) // guess_img.get_height()
  )
  window.blit(guess_img, (
    bottom_bar.get_width()//2 - guess_img.get_width()//2,
    (pygame.display.get_window_size()[1] - bottom_bar.get_height()) + (guess_padding[0])
  ))

def get_card_pressed(mouse, deck): # returns card clicked, else None
  for col in deck:
    for card in col:
      xm, ym = mouse
      x1, y1 = card.bounds[0]
      x2, y2 = card.bounds[1]
      if x1 <= xm <= x2 and y1 <= ym <= y2:
        return card
  return None

def handle_guess(opened, guesses, deck, deck_size, timestamp, fps, sleep_timestamp, sleeping):
  if len(opened) == 2:

    if len(set([i.get_property("type") for i in opened])) == 1: # checks if cards have same type

      guesses += 1

      if opened[0].get_property("strap") == "chain" or opened[1].get_property("strap") == "chain": # checks if any card in the pair has a chain strap

        chained_card = deck[random.randint(0, deck_size[0] - 1)][random.randint(0, deck_size[1] - 1)] # pick random card

        while chained_card.get_property("flipped") and \
          not all([all([j.get_property("flipped") for j in i]) for i in deck]): # failsafe
          chained_card = deck[random.randint(0, deck_size[0] - 1)][random.randint(0, deck_size[1] - 1)]
        
        chained_card_type = chained_card.get_property("type") # get chained card type

        for col in deck:
          for card in col:
            if card.get_property("type") == chained_card_type:
              chained_card.set_property("strap", None)
              chained_card.update_assets()
              chained_card.open()
              card.set_property("strap", None)
              card.update_assets()
              card.open()
      
      for i in opened:
        i.set_property("strap", None)
        i.update_assets()

      sleeping = False

      return [], guesses

    else:
      if not timestamp <= sleep_timestamp + 1 * fps:
        guesses += 1
        sleeping = False
        for i in opened:
          i.close()
        return [], guesses

  return opened, guesses

def get_text_image(font, text, color=0xffffff):
  chars = list(text.lower())
  char_size = pygame.image.load(f"assets/ui/font/{font}/.png").convert_alpha().get_size()
  char_space = 1
  chars_img_size = (char_size[0] * len(chars) + char_space * (len(chars) - 1), char_size[1])
  chars_img = pygame.Surface(chars_img_size)

  rename = {
    " ": "",
    ":": "colon",
    "/": "forward_slash",
    "\\": "backward_slash",
    "<": "less_than",
    ">": "greater than"
  }

  for i, c in enumerate(chars):
    char_img = pygame.image.load(f"assets/ui/font/{font}/{rename.get(c, c)}.png").convert_alpha()
    chars_img.blit(char_img, ((i * char_size[0]) + (i * char_space), 0))

  chars_pxl = pygame.PixelArray(chars_img)
  chars_pxl.replace(0xf2fffa, color)

  chars_img = chars_pxl.make_surface()
  chars_pxl.close()

  return chars_img

def main():
  running = True

  state = "menu"
  initiated = False

  frame = 0
  guesses = 0

  while running:
    frame += 1
    
    pygame.display.set_caption(f"Discarded")

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if event.type == pygame.KEYDOWN:
        if state == "win":
          if event.key == pygame.K_ESCAPE:
            running = False
            sys.exit()
          if event.key == pygame.K_r:
            state = "play"
      if event.type == pygame.MOUSEBUTTONDOWN:
        if state == "menu":
          state = "play"
        elif state == "play":
          if not sleeping:
            card_pressed = get_card_pressed(pygame.mouse.get_pos(), deck)
            if card_pressed and not card_pressed.get_property("flipped"):
              card_pressed.open()
              opened.append(card_pressed)
        elif state == "win":
          state = "play"

    clock.tick(FPS)

    window.fill(0x000000)

    if state == "menu":
      draw_menu_window(frame)
    if state == "play" and not initiated:
      deck = generate_cards(DECK_SIZE)

      opened = []
      guesses = 0

      sleep_timestamp = 0
      sleeping = False
      initiated = True

    if state == "play" and initiated:
      draw_playing_window(deck, DECK_SIZE, guesses)

      if len(opened) == 2 and not sleeping:
        sleep_timestamp = frame
        sleeping = True
      if len(opened) == 0:
        sleep_timestamp = 0
        sleeping = False

      opened, guesses = handle_guess(opened, guesses, deck, DECK_SIZE, frame, FPS, sleep_timestamp, sleeping)
    
      if all([all([j.get_property("flipped") for j in i]) for i in deck]):
        state = "win"
        initiated = False
    
    if state == "win":
      draw_win_window(guesses)

    pygame.display.update()

main()