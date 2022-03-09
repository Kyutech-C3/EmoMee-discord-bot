import discord
import requests
import os
from exception import RoomCreateException, JoinUserException, ExitUserException, DeleteRoomException

emo_mee_api_base_url = os.environ.get('EMOMEE_API_BASE_URL')
emo_mee_client_base_url = os.environ.get('EMOMEE_CLIENT_BASE_URL')

# ルーム作成
def create_room(guild_id: int, user_vc_id: int, user_name: str, room_list: object, limit: int = 0) -> str:
  try:
    print(emo_mee_api_base_url)
    print("guild_id", guild_id, "vc_id", user_vc_id, "limit", limit)
    payload = { "guild_id": guild_id, "vc_id": user_vc_id, "limit": limit }
    res = requests.post(emo_mee_api_base_url, json=payload)
    print(res.status_code)
    create_room_response = res.json()
    print('create_room_response', create_room_response)
  except requests.exceptions.RequestException as e:
    raise RoomCreateException('ルームの作成に失敗しました', e)
  else:
    if res.status_code == 200:
      room_list[str(guild_id) + str(user_vc_id)] = {}
      room_list[str(guild_id) + str(user_vc_id)]['emo_mee_room_id'] = create_room_response['room_id']
      room_list[str(guild_id) + str(user_vc_id)]['user_list'] = []
      print('roomの作成に成功しました', create_room_response['room_id'])
      return emo_mee_client_base_url + '/' + room_list[str(guild_id) + str(user_vc_id)]['emo_mee_room_id'] + '?user_name=' + user_name
    return ''

# ユーザー参加
def join_user(guild_id: int, user_vc_id: int, user_name: str, room_list: object):
  try:
    res = requests.post(emo_mee_api_base_url + '/' + room_list[str(guild_id) + str(user_vc_id)]['emo_mee_room_id'] + '/user', json={ "user_id": user_vc_id, "name": user_name })
    print(res.status_code)
    join_user_response = res.json()
  except requests.exceptions.RequestException as e:
    raise JoinUserException('roomの作成に失敗しました', e)
  else:
    room_list[str(guild_id) + str(user_vc_id)]['user_list'].append(join_user_response)
    print('ユーザーの参加が成功しました', join_user_response)

# ユーザー退出
def exit_user(guild_id: int, user_vc_id: int, user_id: str, room_list: object):
  try:
    print(emo_mee_api_base_url + '/' + room_list[str(guild_id) + str(user_vc_id)]['emo_mee_room_id'] + '/user/' + user_id + '/delete')
  except requests.exceptions.RequestException as e:
    raise ExitUserException('roomの作成に失敗しました', e)
  else:
    for (user, index) in room_list[str(guild_id) + str(user_vc_id)]['user_list']:
      if user.user_id is user_id:
        del room_list[str(guild_id) + str(user_vc_id)]['user_list'][index]
        print('ユーザーの退出が成功しました', user)
        break

# ルーム削除
def delete_room(guild_id: int, user_vc_id: int, room_list: object):
  try:
    res = requests.delete(emo_mee_api_base_url + '/' + room_list[str(guild_id) + str(user_vc_id)]['emo_mee_room_id'])
    print(res.status_code)
    join_user_response = res.json()
    print(join_user_response)
  except requests.exceptions.RequestException as e:
    raise DeleteRoomException('ルームの削除に失敗しました', e)
  else:
    del room_list[str(guild_id) + str(user_vc_id)]
    print('ルームの削除が成功しました')
