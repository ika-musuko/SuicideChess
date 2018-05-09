class PlayerException(Exception):
    '''
    base class for all player manager exceptions
    '''
    pass

class PlayerNotFound(PlayerException):
    '''
    raise this exception if the player you're looking for is not found
    '''
    pass