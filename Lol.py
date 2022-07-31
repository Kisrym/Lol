class Lol:
    def __init__(self, KEY, summonerId, summonerName, puuid, level, icon):
        """Definido os atributos da player

        Args:
            KEY (str): Riot API Key do usuário
            summonerId (str): Id do player
            summonerName (str): Nome do player
            puuid (str): Puuid do player
            level (int): Level do player
            icon (int): Código do icon do player
        """
        import requests
        self.requests = requests
        self.__KEY = KEY
        self.id = summonerId
        self.name = summonerName
        self.puuid = puuid
        self.level = int(level)
        self.icon = int(icon)

    @classmethod
    def player(cls, KEY, *, name):
        """Cria um objeto do tipo Lol com todas as informações do jogador

        Args:
            KEY (str): Riot API Key do usuário
            name (str): Nome do player
            
        Raises:
            KeyError: Se o player não for encontrado.

        Returns:
            class '__main__.Lol: Retorna um objeto do tipo Lol
        """ 
        import requests
        try:
            r = requests.get(f"https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name.lower().replace(' ', '')}?api_key={KEY}").json()
            return cls(KEY, r['id'], r['name'], r['puuid'], r['summonerLevel'], r['profileIconId'])
        except KeyError:
            raise KeyError("Player não encontrado.")

    def __champ(self, id:int):
        r = self.requests.get("http://ddragon.leagueoflegends.com/cdn/12.1.1/data/pt_BR/champion.json").json()['data']
        for c in r:
            if int(r[c]['key']) == id:
                return c

    def __define(self, *, champion):
        taporra = {
            "Aurelionsol":"AurelionSol",
            "Drmundo":"DrMundo",
            "Jarvaniv":"JarvanIV",
            "Kogmaw":"KogMaw",
            "Wukong":"MonkeyKing",
            "Xinzhao":"XinZhao",
            "Reksai":"RekSai",
            "Bardo":"Bard",
            "Masteryi":"MasterYi",
            "Missfortune":"MissFortune"
        }
        champion = champion.capitalize().replace(" ", "")
        if champion in taporra.keys():
            return taporra[champion]
        else:
            return champion

    def rotation(self):
        """Retorna a rotação de campeões da semana

        Returns:
            list: Lista dos campeões
        """
        r = self.requests.get(f"https://br1.api.riotgames.com/lol/platform/v3/champion-rotations?api_key={self.__KEY}").json()
        return [self.__champ(int(x)) for x in r["freeChampionIds"]]

    def masteries(self, /, k=5, *, champ=''):
        """Retorna as maestrias dos champions

        Args:
            k (int, Opcional): Quantidade de champions que a função vai retornar. Default: 5
            champ (str, Optional): Nome do champion que deseja ver a maestria. Default: ''

        Raises:
            KeyError: Se o campeão não for encontrado

        Returns:
            dict: Retorna um dicionário com os dados dos campeões e suas maestrias
        """
        if champ == '':
            return self.requests.get(f"https://br1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{self.id}?api_key={self.__KEY}").json()[:k]
        else:
            try:
                id = self.requests.get("http://ddragon.leagueoflegends.com/cdn/12.1.1/data/en_US/champion.json").json()['data'][self.__define(champion=champ.replace(" ", "").replace("'", "").capitalize())]['key']
                return self.requests.get(f"https://br1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{self.id}/by-champion/{id}?api_key={self.__KEY}").json()
            except KeyError:
                raise KeyError("Champion not found.")
    
    def champion(self, *, champ):
        """Retorna informações sobre um campeão

        Args:
            champ (str): Nome do campeão

        Returns:
            dict: Um dicionário com todas as informações do campeão
        """
        champ = self.__define(champion = champ.replace(" ", "").replace("'", "").capitalize())
    
        return self.requests.get("http://ddragon.leagueoflegends.com/cdn/12.2.1/data/pt_BR/champion.json").json()["data"][f"{champ}"]
    
    def rank(self, playerId = None):
        """Retorna as informações de ranqueada do player

        Args:
            playerId (str, opcional): Id do player. Default: self.id

        Returns:
            list: Uma lista com as informações de ranqueada
        """
        if playerId == None: playerId = self.id
        
        return self.requests.get(f"https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{playerId}?api_key={self.__KEY}").json()


# EXEMPLO
jogador1 = Lol.player(KEY="SEU-TOKEN", name="kainhogameplays")
print(jogador1.rank())