import discord
import asyncio

TOKEN = "Bỏ token bot vào đây"
intents = discord.Intents.all()
# Khởi chạy bot với intents được chỉ định
client = discord.Client(intents=intents)

# Lưu trữ thông tin về người dùng và kênh voice
user_channels = {}

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_voice_state_update(member, before, after):
    if after.channel and after.channel != before.channel:
        if member != client.user and after.channel.id == thay_id_channel_vào_đây:
            # Người dùng tham gia kênh thoại đã chỉ định
            await create_voice_channel(client, member, after.channel)
    elif not after.channel and member.id in user_channels:
        # Người dùng thoát kênh thoại
        channel = user_channels[member.id]
        # Kiểm tra xem không còn ai trong kênh voice
        if len(channel.members) == 0:
            # Xóa kênh voice nếu không còn ai trong đó
            await channel.delete()
        del user_channels[member.id]

@client.event
async def create_voice_channel(client, member, channel):
    channel_name = member.name

    if member.id not in user_channels:
        new_channel = await channel.category.create_voice_channel(
            name=channel_name,
            user_limit=channel.user_limit
        )

        await member.move_to(new_channel)

        user_channels[member.id] = new_channel

        await new_channel.send(
            """Dưới đây là hướng dẫn các lệnh của bot:
            * **!limit <số lượng người>:** Chỉnh giới hạn số người trong kênh voice.
            * **!name <tên kênh mới>:** Chỉnh tên kênh voice.
            Chỉ chủ của kênh voice mới được sử dụng các lệnh này. Để kiểm tra xem bạn có phải là chủ của kênh voice hay không, hãy kiểm tra xem tên người dùng của bạn có hiển thị bên cạnh biểu tượng dấu kiểm màu xanh lá cây hay không."""
        )


# Hàm xử lý khi người dùng gửi tin nhắn
@client.event
async def on_message(message):
    # Kiểm tra xem tin nhắn có chứa lệnh chỉnh giới hạn số người trong kênh voice hay không
    if message.content.startswith("!limit"):
        # Lấy số người giới hạn từ tin nhắn
        limit = int(message.content.split(" ")[1])

        # Kiểm tra xem người gửi tin nhắn có phải là chủ của kênh voice hay không
        if message.author.voice and message.author.voice.channel == user_channels.get(message.author.id):
            # Kiểm tra xem tin nhắn được gửi từ phần chat của kênh voice hay không
            if message.author.voice.channel.category_id == message.channel.category_id:
                # Chỉnh giới hạn số người trong kênh voice
                await message.author.voice.channel.edit(user_limit=limit)
            else:
                # Trả về thông báo lỗi
                await message.reply("Lệnh chỉ được sử dụng trong phần chat của kênh voice.")
        else:
            # Trả về thông báo lỗi
            await message.reply("Chỉ chủ của kênh voice mới được sử dụng lệnh này.")

    # Kiểm tra xem tin nhắn có chứa lệnh chỉnh tên kênh voice hay không
    if message.content.startswith("!name"):
        # Lấy tên kênh voice mới từ tin nhắn
        new_name = message.content.split(" ", 1)[1]

        # Kiểm tra xem người gửi tin nhắn có phải là chủ của kênh voice hay không
        if message.author.voice and message.author.voice.channel == user_channels.get(message.author.id):
            # Kiểm tra xem tin nhắn được gửi từ phần chat của kênh voice hay không
            if message.author.voice.channel.category_id == message.channel.category_id:
                # Chỉnh tên kênh voice
                await message.author.voice.channel.edit(name=new_name)
            else:
                # Trả về thông báo lỗi
                await message.reply("Lệnh chỉ được sử dụng trong phần chat của kênh voice.")
        else:
            # Trả về thông báo lỗi
            await message.reply("Chỉ chủ của kênh voice mới được sử dụng lệnh này.")


# Kết nối bot
client.run(TOKEN)
