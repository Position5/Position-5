import os
from discord.ext import commands


class Cricket(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='cricket',
        description='cricket commands'
    )
    async def cricket_command(self, ctx):
        text = ctx.message.content[len(ctx.prefix) + len(ctx.invoked_with):].strip()

        com, par = text.split(' ', 1)

        if com == 'matches':
            pass
        elif com == 'live':
            pass
        elif com == 'calendar':
            pass
        elif com == 'score':
            pass
        elif com == 'stats':
            pass
        elif com == 'player':
            pass
        else:
            await ctx.send(content='Wrong command')
        return

from aiohttp import ClientSession
import time

class Cricbuzz():
	def __init__(self):
		pass

	async def crawl_url(self,url):
		try:
			async with ClientSession() as session:
				async with session.get(url) as response:
					r = await response.json()
					return r
		except Exception:
			raise

	async def players_mapping(self,mid):
		url = "http://mapps.cricbuzz.com/cbzios/match/" + mid
		match = await self.crawl_url(url)
		players = match.get('players')
		d = {}
		for p in players:
			d[int(p['id'])] = p['name']
		t = {}
		t[int(match.get('team1').get('id'))] = match.get('team1').get('name')
		t[int(match.get('team2').get('id'))] = match.get('team2').get('name')
		return d,t

	async def matchinfo(self,mid):
		d = {}
		d['id'] = mid
		url = "http://mapps.cricbuzz.com/cbzios/match/" + mid
		match = await self.crawl_url(url)

		d['srs'] = match.get('series_name')
		d['mnum'] = match.get('header',).get('match_desc')
		d['type'] = match.get('header').get('type')
		d['mchstate'] = match.get('header').get('state')
		d['status'] = match.get('header').get('status')
		d['venue_name'] = match.get('venue').get('name')
		d['venue_location'] = match.get('venue').get('location')
		d['toss'] = match.get('header').get('toss')
		d['official'] = match.get('official')
		d['start_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(match.get('header').get('start_time'))))


		#squads
		p_map,_ = await self.players_mapping(mid)
		team1 = {}
		team1['name'] = match.get('team1').get('name')
		t1_s = match.get('team1').get('squad')
		if t1_s is None:
			t1_s = []
		team1['squad'] = [ p_map[id] for id in t1_s]
		t1_s_b = match.get('team1').get('squad_bench')
		if t1_s_b is None:
			t1_s_b = []
		team1['squad_bench'] =	[ p_map[id] for id in t1_s_b]
		team2 = {}
		team2['name'] = match.get('team2').get('name')
		t2_s = match.get('team2').get('squad')
		if t2_s is None:
			t2_s = []
		team2['squad'] = [ p_map[id] for id in t2_s]
		t2_s_b = match.get('team2').get('squad_bench')
		if t2_s_b is None:
			t2_s_b = []
		team2['squad_bench'] =	[ p_map[id] for id in t2_s_b]
		d['team1'] = team1
		d['team2'] = team2
		return d

	async def matches(self):
		url = "http://mapps.cricbuzz.com/cbzios/match/livematches"
		crawled_content = await self.crawl_url(url)
		matches = crawled_content['matches']
		info = []

		for match in matches:
			info.append(await self.matchinfo(match['match_id']))
		return info

	async def find_match(self,id):
		url = "http://mapps.cricbuzz.com/cbzios/match/livematches"
		crawled_content = await self.crawl_url(url)
		matches = crawled_content['matches']

		for match in matches:
			if match['match_id'] == id:
				return match
		return None

	async def livescore(self,mid):
		data = {}
		try:
			comm = await self.find_match(mid)
			if comm is None:
				return data
			batting = comm.get('bat_team')
			if batting is None:
				return data
			bowling = comm.get('bow_team')
			batsman = comm.get('batsman')
			bowler = comm.get('bowler')

			team_map = {}
			team_map[comm["team1"]["id"]] = comm["team1"]["name"]
			team_map[comm["team2"]["id"]] = comm["team2"]["name"]

			if batsman is None:
				batsman = []
			if bowler is None:
				bowler = []
			d = {}
			d['team'] = team_map[batting.get('id')]
			d['score'] = []
			d['batsman'] = []
			for player in batsman:
				d['batsman'].append({'name':player['name'],'runs': player['r'],'balls':player['b'],'fours':player['4s'],'six':player['6s']})
			binngs = batting.get('innings')
			if binngs is None:
				binngs = []
			for inng in binngs:
				d['score'].append({'inning_num':inng['id'], 'runs': inng['score'],'wickets':inng['wkts'],'overs':inng['overs'],'declare':inng.get('decl')})
			data['batting'] = d
			d = {}
			d['team'] = team_map[bowling.get('id')]
			d['score'] = []
			d['bowler'] = []
			for player in bowler:
				d['bowler'].append({'name':player['name'],'overs':player['o'],'maidens':player['m'],'runs':player['r'],'wickets':player['w']})
			bwinngs = bowling.get('innings')
			if bwinngs is None:
				bwinngs = []
			for inng in bwinngs:
				d['score'].append({'inning_num':inng['id'], 'runs': inng['score'],'wickets':inng['wkts'],'overs':inng['overs'],'declare':inng.get('decl')})
			data['bowling'] = d
			return data
		except Exception:
			raise

	async def commentary(self,mid):
		data = {}
		try:
			url =  "http://mapps.cricbuzz.com/cbzios/match/" + mid + "/commentary"
			comm = await self.crawl_url(url)
			comm = comm.get('comm_lines')
			d = []
			for c in comm:
				if "comm" in c:
					d.append({"comm":c.get("comm"),"over":c.get("o_no")})
			data['commentary'] = d
			return data
		except Exception:
			raise

	async def scorecard(self,mid):
		try:
			url = "http://mapps.cricbuzz.com/cbzios/match/" +  mid + "/scorecard.json"
			scard = await self.crawl_url(url)
			p_map,t_map = await self.players_mapping(mid)

			innings = scard.get('Innings')
			data = {}
			d = []
			card = {}
			for inng in innings:
				card['batteam'] = inng.get('bat_team_name')
				card['runs'] = inng.get('score')
				card['wickets'] = inng.get('wkts')
				card['overs'] = inng.get('ovr')
				card['inng_num'] = inng.get('innings_id')
				extras = inng.get("extras")
				card["extras"] = {"total":extras.get("t"),"byes":extras.get("b"),"lbyes":extras.get("lb"),"wides":extras.get("wd"),"nballs":extras.get("nb"),"penalty":extras.get("p")}
				batplayers = inng.get('batsmen')
				if batplayers is None:
					batplayers = []
				batsman = []
				bowlers = []
				fow = []
				for player in batplayers:
					status = player.get('out_desc')
					p_name = p_map[int(player.get('id'))]
					batsman.append({'name':p_name,'runs': player['r'],'balls':player['b'],'fours':player['4s'],'six':player['6s'],'dismissal':status})
				card['batcard'] = batsman
				card['bowlteam'] = t_map[int(inng.get("bowl_team_id"))]
				bowlplayers = inng.get('bowlers')
				if bowlplayers is None:
					bowlplayers = []
				for player in bowlplayers:
					p_name = p_map[int(player.get('id'))]
					bowlers.append({'name':p_name,'overs':player['o'],'maidens':player['m'],'runs':player['r'],'wickets':player['w'],'wides':player['wd'],'nballs':player['n']})
				card['bowlcard'] = bowlers
				fall_wickets = inng.get("fow")
				if fall_wickets is None:
					fall_wickets = []
				for p in fall_wickets:
					p_name = p_map[int(p.get('id'))]
					fow.append({"name":p_name,"wkt_num":p.get("wkt_nbr"),"score":p.get("score"),"overs":p.get("over")})
				card["fall_wickets"] = fow
				d.append(card.copy())
			data['scorecard'] = d
			return data
		except Exception:
			raise

	async def fullcommentary(self,mid):
		data = {}
		try:
			url =  "https://www.cricbuzz.com/match-api/"+mid+"/commentary-full.json"
			comm = await self.crawl_url(url)
			comm = comm.get('comm_lines')
			d = []
			for c in comm:
				if "comm" in c:
					d.append({"comm":c.get("comm"),"over":c.get("o_no")})
			data['fullcommentary'] = d
			return data
		except Exception:
			raise

	async def players(self,mid):
		data = {}
		try:
			url =  "https://www.cricbuzz.com/match-api/"+mid+"/commentary.json"
			players = await self.crawl_url(url)
			players = players.get('players')
			d = []
			for c in players:
				if "player" in c:
					d.append({"id":c.get("id"),"f_name":c.get("f_name"),"name":c.get("name"),"bat_style":c.get("bat_style"),"bowl_style":c.get("bowl_style")})
			data['players'] = d
			return data
		except Exception:
			raise

def setup(bot):
    bot.add_cog(Cricket(bot))
