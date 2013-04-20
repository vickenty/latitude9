import pyglet

def _load(name):
    try:
        return pyglet.resource.media(name + '.wav', streaming=False)
    except:
        return None

sounds = [ 'dig', 'explosion', 'fall', 'goal', 'mine', 'pick' ]
cache = dict((name, _load(name)) for name in sounds)

def play(name, vol=0.7):
    sound = cache[name]
    if sound is not None:
        player = sound.play()
        player.vol = vol
