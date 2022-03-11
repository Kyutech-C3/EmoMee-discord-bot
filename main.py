import os
from dotenv import load_dotenv
import discord
from cruds import create_room, delete_room, join_user, exit_user, genalate_join_url
from exception import RoomCreateException, JoinUserException, ExitUserException, AlreadyExistsException
from globalData import watchChannelList

load_dotenv()
TOKEN = os.environ.get('TOKEN')
GUILD_ID = os.environ.get('GUILD_ID')
EMO_MEE_CLIENT_BASE_URL = os.environ.get('EMOMEE_CLIENT_BASE_URL')

intents = discord.Intents.default()  # デフォルトのIntentsオブジェクトを生成
intents.typing = False
client = discord.Bot()
clientClient = discord.Client(intents=intents)

hoge: discord.ApplicationContext


@client.event
async def on_ready():
  print('sintyokuBot is running')

# 入退室
@client.event
async def on_voice_state_update(member, before, after):
  if str(member.guild.id) in watchChannelList:
    if before.channel != after.channel:
      # 退室
      if before.channel is not None and before.channel.id in watchChannelList[str(member.guild.id)]:
        try:
          exit_user(member.guild.id, before.channel.id, member.id)
          return
        except ExitUserException as e:
          print(e)
          return
      # 入室
      if after.channel is not None and after.channel.id in watchChannelList[str(member.guild.id)]:
        try:
          join_res = join_user(member.guild.id, after.channel.id, member.id, member.name)
          if join_res['status']:
            await member.send(f"EmoMee参加URL: {genalate_join_url(join_res['room_id'], join_res['user_id'])}")
          else:
            return
        except JoinUserException as e:
          print(e)
          await member.send("ルームへの参加に失敗し、参加URLが発行できませんでした...\n再度VCに入り直してください.")

# EmoMee Botの連携を開始する
@client.slash_command(description='EmoMeeの使用', guild_ids=[int(GUILD_ID)])
async def start_emomee(ctx: discord.ApplicationContext, limit: discord.Option(str, 'roomの有効期限を設定してください') = '24'):
  guild_id = ctx.guild_id
  guild = ctx.guild
  # channel_id = ctx.channel_id
  # channel = ctx.channel
  # print(guild.members, guild_id)

  if guild_id is None:
    await ctx.respond('ギルド情報の取得に失敗しました')
  else:
    if ctx.author.voice is None:
      await ctx.respond('VCに参加してから実行してください')
    else:
      user_vc_id = ctx.author.voice.channel.id
      user_vc_name = ctx.author.voice.channel.name
      vc_member_id_list = list(ctx.author.voice.channel.voice_states.keys())

  # hoge = list(clientClient.get_all_members())
  # user_id = ctx.author.id
  # user_name = ctx.author.display_name

  # users = client.users

  # print(discord.utils.get(users, id=user_id))
  # print(clientClient.get_channel(user_vc_id), user_vc_members, hoge)

      # ルーム作成
      try:
        room_id = create_room(guild_id, user_vc_id, limit)
      except RoomCreateException as e:
        print('Error', e)
        await ctx.respond(e)
      except AlreadyExistsException as e:
        print('Error', e)
        await ctx.respond(e)
      else:
        if (str(guild_id) in watchChannelList):
          if (user_vc_id in watchChannelList[str(guild_id)]):
            watchChannelList[str(guild_id)].append(user_vc_id)
        else:
          watchChannelList[str(guild_id)] = [user_vc_id]
        await ctx.respond('ルームが作成されました。\nルームID:`'+ room_id +'`')
      # delete_room(guild_id, user_vc_id)

        # ユーザー参加（すでにVCにいるユーザー）
        for vc_member_id in vc_member_id_list:
          user = await client.fetch_user(vc_member_id)
          try:
            join_res = join_user(guild_id, user_vc_id, vc_member_id, user.name)
            if join_res['status']:
              await user.send(f"**ギルド: {guild} VC: {user_vc_name}**\nEmoMee参加URL: {genalate_join_url(join_res['room_id'], join_res['user_id'])}")
            else:
              return
          except JoinUserException as e:
            print(e)
            await user.send('ルームへの参加に失敗しました. 参加URLを取得する場合は再度VCに入り直してください.')
          print(user)
  return

def run_bot(token: str):
  try:
    client.run(token)
  except Exception as e:
    print(e)

run_bot(TOKEN)
