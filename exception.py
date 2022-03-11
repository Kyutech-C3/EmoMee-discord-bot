class RoomCreateException(Exception):
    """ルームの作成中にエラーが発生したことを知らせる例外クラス"""
    pass

class AlreadyExistsException(Exception):
    """ルームがすでに存在していることを知らせる例外クラス"""
    pass

class JoinUserException(Exception):
    """ユーザーの参加中にエラーが発生したことを知らせる例外クラス"""
    pass

class ExitUserException(Exception):
    """ユーザーの退出中にエラーが発生したことを知らせる例外クラス"""
    pass

class DeleteRoomException(Exception):
    """ルームの削除中にエラーが発生したことを知らせる例外クラス"""
    pass