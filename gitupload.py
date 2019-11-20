"""
GITHUB File Uploader Plugin for userbot. Heroku Automation should be Enabled. Else u r not that lazy // For lazy people
Instructions:- Set GITHUB_ACCESS_TOKEN and GIT_GIT_REPO_NAME Variables in Heroku vars First
usage:- .commit reply_to_any_plugin //can be any type of file too. but for plugin must be in .py 

"""


from github import Github
import aiohttp
import asyncio
import os
import time
import glob
from datetime import datetime
from telethon import events
from telethon.tl.types import DocumentAttributeVideo
from uniborg.util import admin_cmd, humanbytes, progress, time_formatter

GIT_TEMP_DIR = "./github/"
@borg.on(admin_cmd(pattern=".commit ?(.*)", allow_sudo=True))
async def download(event):
	global reponame
	reponame = Config.GIT_REPO_NAME
	if reponame is None:
		reponame = event.pattern_match.group(1)
	if not reponame and Config.GIT_REPO_NAME is None:
		await event.edit("`Please ADD a proper repo name from Vars or specify your repo name as in the example: .commit <reponame>`")
		return
	if event.fwd_from:
		return	
	if Config.GITHUB_ACCESS_TOKEN is None:
		await event.edit("`Please ADD a proper access token from github.com`") 
		return   
	if Config.GIT_USER_NAME is None:
		await event.edit("`Please ADD a proper github username from vars`")
		return 
	mone = await event.reply("Processing ...")
	if not os.path.isdir(GIT_TEMP_DIR):
		os.makedirs(GIT_TEMP_DIR)
	start = datetime.now()
	reply_message = await event.get_reply_message()
	try:
		c_time = time.time()
		downloaded_file_name = await borg.download_media(
			reply_message,
			GIT_TEMP_DIR,
			progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
			progress(d, t, mone, c_time, "trying to download")
			)
		)
	except Exception as e: 
		await mone.edit(str(e))
	else:
		end = datetime.now()
		ms = (end - start).seconds
		await event.delete()
		await mone.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
		await mone.edit("Committing to Github....")
		await git_commit(downloaded_file_name,mone)
		
async def git_commit(file_name,mone):
	content_list = []
	access_token = Config.GITHUB_ACCESS_TOKEN
	g = Github(access_token)
	file = open(file_name,"r",encoding="utf-8")
	commit_data = file.read()
	if Config.GIT_REPO_NAME is not None:
		repo = g.get_repo(Config.GIT_USER_NAME + "/" + reponame)
	else:
		repo = g.get_repo(Config.GIT_USER_NAME + "/" + reponame)
	print(repo.name)
	create_file = True
	contents = repo.get_contents("")
	for content_file in contents:
		content_list.append(str(content_file))
		print(content_file)
	for i in content_list:
		create_file = True
		if i == 'ContentFile(path="'+file_name+'")':
			return await mone.edit("`File Already Exists`")
			create_file = False
	file_name = file_name		
	if create_file == True:
		file_name = file_name.replace("./github/","")
		print(file_name)
		repo.create_file(file_name, "Uploaded New Plugin", commit_data, branch="master")
		print("Committed File")
		try:
			files = glob.glob('github/*')
			for f in files:
				os.remove(f)
			link =  "https://github.com/" + Config.GIT_USER_NAME + "/" + reponame + "/blob/master/" + file_name
			rawlink = "https://raw.githubusercontent.com/" + Config.GIT_USER_NAME + "/" + reponame + "/master/" + file_name
			await mone.edit("`Committed on Your Github Repo.`\n\nLink: `" + link + "`\n\nRAW Link: `" + rawlink + "`")
		except:
			print("Cannot Create Plugin")
			await mone.edit("Cannot Upload Plugin")
	else:
		return await mone.edit("`Committed Suicide`")


	
