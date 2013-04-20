import pyglet

sounds = [ 'dig', 'explosion', 'fall', 'goal', 'mine', 'pick' ]
cache = dict((name, pyglet.resource.media(name + '.wav', streaming=False)) for name in sounds)

def play(name, vol=0.7):
    sound = cache[name]
    player = sound.play()
    player.vol = vol
