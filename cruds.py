import discord
import requests
import os
from exception import RoomCreateException, JoinUserException, ExitUserException, DeleteRoomException, AlreadyExistsException

EMO_MEE_API_BASE_URL = os.environ.get('EMOMEE_API_BASE_URL')
EMO_MEE_CLIENT_BASE_URL = os.environ.get('EMOMEE_CLIENT_BASE_URL')

# ルーム作成
def create_room(guild_id: int, user_vc_id: int, limit: int = 0) -> str:
  try:
    print(EMO_MEE_API_BASE_URL)
    print("guild_id", guild_id, "vc_id", user_vc_id, "limit", limit)
    payload = { "guild_id": guild_id, "vc_id": user_vc_id, "limit": limit }
    res = requests.post(EMO_MEE_API_BASE_URL, json=payload)
    print(res.status_code)
    create_room_response = res.json()
    print('create_room_response', create_room_response)
  except requests.exceptions.RequestException as e:
    raise RoomCreateException('ルームの作成に失敗しました', e)
  else:
    if res.status_code == 200:
      print('roomの作成に成功しました', create_room_response['room_id'])
      return create_room_response['room_id']
    elif res.status_code == 400:
      raise AlreadyExistsException('ルームがすでに存在します', res.status_code)
    else:
      raise RoomCreateException('ルームの作成に失敗しました', res.status_code)

# ユーザー参加
def join_user(guild_id: int, user_vc_id: int, user_id: int, user_name: str) -> object:
  try:
    res = requests.get(f"{EMO_MEE_API_BASE_URL}?guild_id={str(guild_id)}&vc_id={str(user_vc_id)}")
    # 404返る可能性あり
    room_expired_at = res.json()['expired_at']
    room_id = res.json()['room_id']
    res = requests.post(f"{EMO_MEE_API_BASE_URL}/{room_id}/user", json={ "user_id": user_id, "name": user_name })
    print(res.status_code)
    join_user_response = res.json()
    join_user_id = res.json()['user_id']
  except requests.exceptions.RequestException as e:
    raise JoinUserException('ユーザーの参加に失敗しました', e)
  else:
    if res.status_code == 200:
      print('ユーザーの参加が成功しました', join_user_response)
      return {'status': True, 'room_id': room_id, 'expired_at': room_expired_at, 'user_id': join_user_id}
    elif res.status_code == 400:
      print('すでに参加しています')
      return {'status': False}
    else:
      raise JoinUserException('ユーザーの参加に失敗しました', res.status_code)

# ユーザー退出
def exit_user(guild_id: int, user_vc_id: int, user_id: int):
  try:
    res = requests.get(f"{EMO_MEE_API_BASE_URL}?guild_id={str(guild_id)}&vc_id={str(user_vc_id)}")
    room_id = res.json()['room_id']
    res = requests.delete(f"{EMO_MEE_API_BASE_URL}/{room_id}/user/{str(user_id)}")
  except requests.exceptions.RequestException as e:
    raise ExitUserException('ユーザーの退出に失敗しました', e)
  else:
    print(res)
    if res.status_code == 200:
      print('ユーザーの退出が成功しました', str(user_id))
    else:
      raise ExitUserException('ユーザーの退出が失敗しました', res.status_code)

# ルーム削除
def delete_room(guild_id: int, user_vc_id: int):
  try:
    res = requests.get(f"{EMO_MEE_API_BASE_URL}?guild_id={str(guild_id)}&vc_id={str(user_vc_id)}")
    room_id = res.json()['room_id']
    res = requests.delete(f"{EMO_MEE_API_BASE_URL}/{room_id}")
  except requests.exceptions.RequestException as e:
    raise DeleteRoomException('ルームの削除に失敗しました', e)
  else:
    if res.status_code == 200:
      print('ルームの削除が成功しました')
    else:
      print('ルームの削除に失敗しました')

# 参加URLの生成
def genalate_join_url(room_id: str, discord_user_id: str) -> str:
  return f"{EMO_MEE_CLIENT_BASE_URL}{room_id}?user_id={discord_user_id}"
