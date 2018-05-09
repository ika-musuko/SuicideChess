class UseSetRoomStatus(Exception):
    '''
    exception to raise if you try to set the room status using set_room_attribute
    '''
    pass


class RoomException(Exception):
    '''
    base class for all room exceptions
    '''
    pass


class IncorrectAccessCode(RoomException):
    '''
    raise this exception if an incorrect access code is given for joining a friend room
    '''
    pass


class RoomIsNotYours(RoomException):
    '''
    raise this exception when a user is trying to manipulate a room he is not allowed to
    '''
    pass


class UserAlreadyInRoom(RoomException):
    '''
    raise this exception if a user is already in a room
    '''
    pass


class RoomDoesNotExist(RoomException):
    '''
    raise this exception when a room does not exist
    '''
    pass


class RoomIsInProgress(RoomException):
    '''
    raise this exception when a room is in progress
    '''
    pass


class RoomIsNotWaiting(RoomException):
    '''
    raise this exception if the room is not waiting
    '''
    pass


class RoomIsNotFriend(RoomException):
    '''
    raise this exception when someone is trying to join a non-friend room using the join friend room interface
    '''
    pass