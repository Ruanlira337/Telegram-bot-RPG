import telebot
import random
bot = telebot.TeleBot('token aqui')

#Dicionarios e itens
inv1 = {}
status1 = {}
etapas = {}

# Mensagem inicial
@bot.message_handler(commands=['help', 'ajuda'])
def ini(msg):
  img = "https://imgur.com/a/oxIcZTT"
  bot.send_photo(msg.chat.id, img, caption='''Seja bem vindo ao RPG da ETO!
Código por: Ruan Lira

Guia de comandos:
/iniciar - começa o jogo
/inv - checa seu inventário 
/status - checa HP, level, EXP e Estado(Vivo ou morto)
/sair - desiste do jogo
/curar - usa um curativo no seu personagem(você precisa ter no inventário)

Dados os comandos, vamos iniciar, estou no aguardo!''')

# Função de reset de jogo
def reset(msg):
  user_id = msg.chat.id
  if user_id in status1 and inv1:
    del status1[user_id]
    del etapas[user_id]
    del inv1[user_id]
  elif user_id in status1:
    del status1[user_id]
    del etapas[user_id]

# Sair do jogo 
@bot.message_handler(commands=['sair'])
def sair_do_jogo(msg):
  user_id = msg.chat.id
  if user_id in status1 and inv1:
    del status1[user_id]
    del etapas[user_id]
    del inv1[user_id]
    bot.send_message(user_id, "Seu progresso foi deletado")
    return
  elif user_id in status1:
    del status1[user_id]
    del etapas[user_id]
    bot.send_message(user_id, "Seu progresso foi deletado")
    return
  else:
    bot.send_message(user_id, "Você ainda não iniciou o jogo!\nUse o /iniciar")

# /iniciar + sistema de salvar nome
@bot.message_handler(commands=['iniciar'])
def iniciar(msg):
  url = "https://imgur.com/a/p6XIn3B"
  bot.send_photo(msg.chat.id, url, caption='''Você acorda em uma floresta escura...
"Ei, ei, você tá bem?"
...
"Qual o seu nome criança?"
...
Insira um nome:''')
  bot.register_next_step_handler(msg, save_name)
def save_name(msg):
  user_id = msg.chat.id
  nome = msg.text
  status1[user_id] = {
    'nome': nome,
    'vida': 100,
    'level': 1,
    'exp': 1,
    'status': True, # Vivo ou morto
  }
  etapas[user_id] = 1
  bot.send_message(user_id, f"''Oh... você parece bem sozinho {nome}, não vou te deixar aqui.\nVenha comigo por favor.''\nSeguir o homem misterioso?\n1. Sim\n2. Não ")

# Historia 
@bot.message_handler(func=lambda msg: not msg.text.startswith('/'))
def historia1(msg):
  user_id = msg.chat.id
  escolha = msg.text.strip()
  if user_id not in etapas:
    ini(msg)
    return
  etapa = etapas[user_id]
  dados = status1[user_id]
  nome = status1[user_id]['nome']
  if etapa == 1:
    if escolha == '1':
      etapas[user_id] = 2.1
      bot.send_message(user_id, "O homem te levou até um vilarejo\n''Aguarde aqui criança, chamarei o líder''\nVocê ouve respirações pesadas ao seu redor\nEsperar pelo homem?\n1. Sim\n2. Não")
    elif escolha == '2':
      etapas[user_id] = 2.2
      dados['vida'] -= 20
      bot.send_message(user_id, "''Posso eu deixar uma crinça aqui? Não posso! Venha imediatamente garoto!''\nVocê perde 20 de hp após ser levado a força...")
      bot.send_message(user_id, "O homem te levou até um vilarejo.\n''Aguarde aqui moleque, chamarei o líder''\nVocê ouve respirações pesadas ao seu redor.\nEsperar pelo homem?\n1. Sim\n2. Não")
    else:
      bot.send_message(user_id, "Escolha inválida, digite 1 ou 2")
      return
  elif etapa == 2.1:
    if escolha == '1':
      etapas[user_id] = 3.1
      inv1[user_id] = {
        'Isqueiro': 1,
        'Pedaços de vela': 3,
        'Curativo': 1,
      }
      bot.send_message(user_id, "O homem retornou\n''Siga me, criança''\nEle te leva até uma pequena cabana e antes que você percebesse\n......\nÓtimo, você está preso, pequena criança leiga!")
      bot.send_message(user_id, "Observando o local, você acha um isqueiro, alguns pedaços de vela e um curativo velho(Adicionados ao inventário!)\n\nO que deseja fazer?\n1. Esperar\n2. Procurar por uma brecha de fuga")
    elif escolha == '2':
      etapas[user_id] = 3.2
      bot.send_message(user_id, f"Você espreita a vila, os moradores são bem quietos...\nVocê decide fugir\n''{nome}!!!, não vá, eu imploro pela sua piedade, não me deixe apodrecer!''\n....\nVocê prefere acelerar o passo.")
      bot.send_message(user_id, "Você chegou na saída do vilarejo...\nIr embora?\n1. Sim\n2. Não ")
    else:
      bot.send_message(user_id, "Escolha inválida, digite 1 ou 2")
      return
  elif etapa == 2.2:
    if escolha == '1':
      etapas[user_id] = 3.1
      inv1[user_id] = {
        'Isqueiro': 1,
        'Pedaços de vela': 3,
        'Curativo': 1,
      }
      bot.send_message(user_id, "O homem voltou pra te buscar\n''Vem logo pirralho''\n...\nEle te trancou em uma cabana suja.")
      bot.send_message(user_id, "Observando o local, você acha um isqueiro,alguns pedaços de vela e um curativo velho(Adicionados ao inventário!)\n\nO que deseja fazer?\n1. Esperar\n2. Procurar por uma brecha de fuga")
    elif escolha == '2':
      reset(msg)
      bot.send_message(user_id, "Você tenta fugir\n....\n''Onde pensa que vai pivete!!''\n....\nVocê foi esperto antes, mas não se pode ser esperto sempre, fim da linha:\n\nVOCÊ MORREU!")
      return
    else:
      bot.send_message(user_id, "Escolha inválida, digite 1 ou 2")
      return
  elif etapa == 3.2:
    if escolha == '1':
      reset(msg)
      bot.send_message(user_id, "Você fugiu para a floresta, sem rumo ou direção, apenas lhe resta sucumbir perante a fome...\n\nVOCÊ MORREU")
      return
    elif escolha == '2':
      etapas[user_id] = 4
      inv1[user_id] = {
        "Chave estranha": 1,
      }
      bot.send_message(user_id, "Você prefere ficar e explorar\n...\nEnquanto caminha, você se depara com uma chave estranha no chão\n\nChave adicionada ao inventário!")
      bot.send_message(user_id, "''Ei criança! Te achei finalmente, venha comigo''\n\nPessoas estranhas estão dançando ao seu redor\nVocê chegou no centro de...dança?\nEspere... Você nota um buraco estranho no chão, parece plausível para uma fuga\n1. Seguir o caminho da dança\n2. Correr até o buraco")
    else:
      bot.send_message(user_id, "Escolha inválida, digite 1 ou 2")
      return
  elif etapa == 3.1:
    if escolha == '1':
      etapas[user_id] = 4
      inv1[user_id]["Chave estranha"] = 1
      bot.send_message(user_id, "Após 2 horas de espera...\nVocê foi levado por 2 guardas estranhos até o olho da vila, no caminho você vê uma chave estranha no chão e decide pegar(adicionado ao inventário)\n\nPessoas estranhas estão dançando ao seu redor\nVocê chegou no centro de...dança?\nEspere... Você nota um buraco estranho no chão, parece plausível para uma fuga\n1. Seguir o caminho da dança\n2. Correr até o buraco")
    elif escolha == '2':
      etapas[user_id] = 4
      inv1[user_id]['Chave estranha'] = 1
      status1[user_id]['vida'] -= 20
      del inv1[user_id]["Isqueiro"]
      del inv1[user_id]["Pedaços de vela"]
      bot.send_message(user_id, "Após 2 horas de tentativa você consegue fugir ao criar uma chave de gesso, porém, perde 20 de HP devido queimadura e seu isqueiro/pedaços de vela ficam inúteis\nVocê decide ir ao olho da vila, no caminho você vê uma chave estranha no chão e decide pegar(adicionado ao inventário)\n\nPessoas estranhas estão dançando ao seu redor\nVocê chegou no centro de...dança?\nEspere... Você nota um buraco estranho no chão, parece plausível para uma fuga\n1. Seguir o caminho da dança\n2. Correr até o buraco")
    else:
      bot.send_message(user_id, "Escolha inválida, digite 1 ou 2")
      return
  elif etapa == 4:
    if escolha == '1':
      bot.send_message(user_id, "Ninguém pode ver o futuro é claro, mas você realmente achou que isso seria uma boa ideia?\n\nVOCÊ MORREU TORTURADO!")
      reset(msg)
      return
    elif escolha == '2':
      etapas[user_id] = 5
      dano = random.randint(5, 25)
      status1[user_id]['vida'] -= dano
      inv1[user_id]['Faca estranha'] = 1
      vidaestado = status1[user_id]['vida']
      bot.send_message(user_id, f"Você se machucou e perdeu {dano} de HP, porém fugiu com sucesso!")
      if status1[user_id]['vida'] < 45:
        bot.send_message(user_id, f"CUIDADO! Você está com {vidaestado} de HP!!")
      bot.send_message(user_id, "Você descobre uma grande zona subterrânea,..., tem uma faca no chão,..., você decide que é hora de parar de correr pra tudo(adicionado ao inventário!)\nAndando um pouco, você chega ao que parece ser uma saída, porém, um garoto da sua estatura barra o caminho, ele segura uma faca...\n\n''Te esperei por muito tempo, venha e lute, se me vencer, leve meu corpo aos loucos lá em cima e terá a ajuda que quiser deles''\n\nLutar com o garoto?\n1. Sim\n2. Fugir que nem um cachorro e abandonar sua única chance de viver")
    else:
      bot.send_message(user_id, "Escolha inválida, digite 1 ou 2")
      return
  elif etapa == 5:
    if escolha == '1' or '2':
      etapas[user_id] = 6
      dano = random.randint(20, 45)
      del inv1[user_id]['Faca estranha']
      inv1[user_id]['Faca ensanguentada'] = 1
      status1[user_id]['vida'] -= dano
      if status1[user_id]['vida'] <= 0:
        bot.send_message(user_id, "O mundo é dos fortes, e você foi fraco...\n\nVOCÊ MORREU NO CONFLITO!")
        reset(msg)
        return
      bot.send_message(user_id, f"O garoto te cortou com rapidez, parece que ele nunca teve a intenção de te deixar escolher afinal\nVocês trocam golpes rápidos, WOW! Mas porque você é bom nisso.....?\nA luta foi intensa, mas quem venceu foi você no fim, a custo de {dano} de HP. O garoto, ajoelhado perante você, aceita a morte...\n\nMata-ló?\n1. Sim\n2. Não")
    else:
      bot.send_message(user_id, "Escolha inválida, digite 1 ou 2")
      return
  elif etapa == 6:
    if escolha == '1':
      status1[user_id]['exp'] += 99998
      status1[user_id]['level'] += 98
      xp = status1[user_id]['exp']
      dados = status1[user_id]
      nome = dados['nome']
      vida = dados['vida']
      level = dados['level']
      exp = dados['exp']
      bot.send_message(user_id, f"Oh... Você é apenas um assassino cruel no fim\n\nVocê ganhou {xp} EXP\nA aldeia estranha está sobre sua mão agora, parabéns pequeno monstro!\nSeus STATUS finais:\nNome: {nome}\nVida: {vida}\nLevel: {level}\nEXP: {exp}\nEstado: Louco sanguinário\n\n VOCÊ TERMINOU O JOGO!")
      reset(msg)
      return
    elif escolha == '2':
      bot.send_message(user_id, "...\n''Porque você está me poupando?''\n\nVocê foge da vila, sem EXP, sem nenhum level extravagante, mas com a consciência limpa\nParabéns Herói! Mas a vida é cruel e você morre de fome na floresta\n\nVOCÊ TERMINOU O JOGO!")
      reset(msg)
      return
    else:
      bot.send_message(user_id, "Escolha inválida, digite 1 ou 2")
      return
  
# Comando de cura
@bot.message_handler(commands=['curar'])
def cura(msg):
  user_id = msg.chat.id
  if user_id in inv1:
    inv = inv1[user_id]
    dados = status1[user_id]
    if "Curativo" in inv:
      if inv["Curativo"] == 1:
        del inv["Curativo"]
        cura = random.randint(10, 50)
        dados['vida'] = min(dados.get("vida", 0) + cura, 100)
        bot.send_message(user_id, f"Você recuperou {cura} de HP!")
      if "Curativo" in inv and inv["Curativo"] > 1:
        inv["Curativo"] -= 1
        cura = random.randint(5, 50)
        dados['vida'] = min(dados.get('vida', 0) + cura, 100)
        bot.send_message(user_id, f"Você recuperou {cura} de HP!")
    else:
      bot.send_message(user_id, "Você não tem itens de cura.")
  else:
    if user_id in status1:
      bot.send_message(user_id, "Você não tem itens de cura.")
    else:
      bot.send_message(user_id, "Você não começou o jogo!\nUse o /iniciar")
      
# Mostrar inventário
@bot.message_handler(commands=['inv'])
def mostrar_inv(msg):
  user_id = msg.chat.id
  if user_id in inv1:
    inv = inv1[user_id]
    lista_inv = ""
    for i, (k, v) in enumerate(inv.items(), start = 1):
      lista_inv += f"{i}.{k}({v} unidade{'s' if v != 1 else ''})\n"
    bot.send_message(user_id, f"🎒INVENTÁRIO🎒\n\n{lista_inv}")
  else:
    if user_id not in status1:
      bot.send_message(user_id, "Você ainda não iniciou o jogo!\nUse o /iniciar")
    else:
      bot.send_message(user_id, "Seu inventário está vazio!")
    
# Mostrar status
@bot.message_handler(commands=['status'])
def mostrar_status(msg):
  user_id = msg.chat.id
  if user_id in status1:
    dados = status1[user_id]
    nome = dados['nome']
    vida = dados['vida']
    level = dados['level']
    exp = dados['exp']
    status = "Vivo" if dados['status'] else "Morto"
    bot.send_message(user_id, f'''📜SEUS STATUS📜
    
Nome: {nome}
Vida: {vida}
Level: {level}
EXP: {exp}
Estado: {status}''')
  else:
    bot.send_message(user_id, "Você ainda não iniciou o jogo!\nUse o /iniciar")
  
bot.infinity_polling()