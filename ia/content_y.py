# Atlas de l'IA : chapitre 81, Pipecat et LiveKit Agents (cadres pour agents vocaux, hors ligne et avec RAG). API vérifiées sur pipecat-ai 1.15.0 et livekit-agents 1.8.11 (novembre 2026).
GROUPS = [("Agir : harnais, agents, boucles", ["pipecat"])]
P = lambda q, ch, a, w: dict(q=q, choices=ch, answer=a, why=f"<p>{w}</p>")
def pipe(key, title, sub, stages, plate, facts, per=3, bw=2.3, gap=0.8):
    return dict(key=key, title=title, sub=sub, kind="pipeline", per=per, bw=bw, gap=gap, y=1.4, stages=[dict(n=a, s=b, **({"pal": c} if c else {})) for a, b, c in stages], plate=plate, facts=facts)
L = lambda *a: '<ul class="rules">' + "".join(f"<li>{x}</li>" for x in a) + "</ul>"
CODE = lambda s: '<pre style="font-size:11.5px;line-height:1.35;white-space:pre-wrap;overflow-wrap:anywhere;background:rgba(0,0,0,.04);padding:8px 10px;border-radius:6px;margin:8px 0">' + s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") + "</pre>"
CHAPTERS = [dict(dir="pipecat", no=81, title="Pipecat et LiveKit Agents", sub="deux cadres ouverts pour construire un agent vocal", cnt="Trames et pipeline, sessions et salles, réglages, RAG et fonctionnement hors ligne", alt="Une chaîne de processeurs traversée par des trames audio et texte",
 scenes=[
  pipe("trames", "Pipecat : une chaîne de trames", "tout est une trame qui circule", [("Transport (entrée)", "micro, WebRTC, téléphone", None), ("STT", "audio → TranscriptionFrame", "blue"), ("Agrégateur utilisateur", "VAD, fin de tour, contexte", "red"), ("LLM", "contexte → TextFrame en flux", "blue"), ("TTS", "texte → audio en flux", "blue"), ("Transport (sortie)", "haut-parleur, puis contexte", None)],
       "Dans Pipecat, un agent est une liste de processeurs. Des trames (audio, texte, transcription, contexte, interruption) les traversent dans l’ordre. Chaque processeur transforme les trames qu’il comprend et laisse passer les autres. L’agrégateur utilisateur décide de la fin du tour de parole et envoie le contexte au LLM ; l’agrégateur assistant, en fin de chaîne, enregistre ce qui a vraiment été dit.",
       [["unité", "la trame"], ["agent", "une liste de processeurs"]]),
  pipe("lkarchi", "LiveKit : une salle et des agents", "l’agent est un participant", [("Navigateur, appli, téléphone", "participants humains", None), ("Serveur LiveKit", "salle WebRTC (SFU)", "red"), ("Serveur d’agents", "attend les sessions", "blue"), ("Session", "un processus par conversation", "blue"), ("AgentSession", "STT, LLM, TTS, VAD, tours", "blue"), ("Agent", "consignes, outils, crochets", "red")],
       "LiveKit Agents s’appuie sur un serveur WebRTC, LiveKit (ouvert, auto-hébergeable). L’agent rejoint une « salle » comme un participant. Un serveur d’agents reçoit les demandes, lance un processus par conversation, et chaque processus exécute une AgentSession (les modèles et la gestion des tours) au service d’un Agent (ses consignes, ses outils).",
       [["force", "multi-utilisateurs, téléphonie, montée en charge"], ["coût", "un serveur de plus"]]),
  pipe("compare", "Lequel choisir ?", "deux philosophies", [("Pipecat", "une bibliothèque, un processus", "blue"), ("Transports au choix", "local, WebRTC, WebSocket, téléphonie", "blue"), ("Contrôle fin", "chaque trame est accessible", "blue"), ("LiveKit Agents", "un cadre sur une infrastructure", "red"), ("Salles WebRTC", "plusieurs participants, SIP", "red"), ("Exploitation", "répartition, redémarrage, mesures", "red")],
       "Pipecat est une bibliothèque : tout tient dans un programme Python, avec le transport de son choix, et chaque trame est modifiable. LiveKit Agents est un cadre adossé à une infrastructure temps réel : il apporte les salles, la téléphonie SIP, la répartition des conversations entre machines. Les deux sont sous licence libre et peuvent fonctionner sans aucun service en ligne.",
       [["prototype local", "Pipecat"], ["service à plusieurs", "LiveKit"]]),
  pipe("hors", "Une pile entièrement locale", "sans clé d’API", [("Silero VAD", "voix, CPU", "blue"), ("Smart Turn v3 / turn-detector", "fin de tour, CPU", "blue"), ("faster-whisper", "STT, GPU", "blue"), ("Ollama, llama.cpp, vLLM", "LLM, API compatible OpenAI", "red"), ("Piper, Kokoro", "TTS local", "blue"), ("Speaches", "serveur STT + TTS compatible OpenAI", None)],
       "Pipecat embarque directement des services locaux : Whisper (faster-whisper ou MLX), Piper, Kokoro, Ollama. LiveKit passe le plus souvent par le greffon OpenAI pointé vers un serveur local compatible : Ollama ou vLLM pour le LLM, Speaches (faster-whisper, Kokoro, Piper) pour la voix. Dans les deux cas, la détection de voix et de fin de tour tourne sur le CPU.",
       [["clé", "le format OpenAI en local"], ["GPU", "STT + LLM (+ TTS)"]]),
  pipe("tours", "Fin de tour et interruptions", "les mêmes réglages, deux noms", [("Détection de voix", "Pipecat : VADParams · LiveKit : silero.VAD", "blue"), ("Fin de tour", "Smart Turn v3 · MultilingualModel", "red"), ("Délai mini / maxi", "stop_secs · endpointing", "red"), ("Interruption", "durée et mots minimum", "red"), ("Fausse interruption", "reprendre si ce n’était qu’un bruit", None), ("Génération anticipée", "LLM lancé avant la fin sûre", None)],
       "Les deux cadres combinent une détection de voix rapide et un modèle de fin de tour, qui lit l’audio (Smart Turn) ou le texte (turn-detector de LiveKit) pour juger si la phrase est finie. On règle ensuite des délais minimum et maximum, la durée ou le nombre de mots qui déclenchent une interruption, et la reprise après une fausse interruption.",
       [["Pipecat", "agrégateur utilisateur"], ["LiveKit", "turn_handling"]]),
  pipe("rag", "Où brancher le RAG", "trois emplacements", [("Pipecat : processeur", "entre agrégateur et LLM", "blue"), ("LiveKit : crochet", "on_user_turn_completed", "blue"), ("Les deux : outil", "fonction « chercher »", "red"), ("Injection", "à chaque tour, rapide", "blue"), ("Outil", "le LLM décide, plus lent", "red"), ("Dans tous les cas", "passages courts, source dite", None)],
       "Le RAG s’insère juste avant le LLM : un processeur Pipecat qui enrichit le contexte, ou le crochet on_user_turn_completed de LiveKit. Autre voie : déclarer une fonction « chercher dans les notes » que le LLM appelle lui-même ; plus souple, mais un aller-retour de plus, donc plus lent à l’oral.",
       [["rapide", "injection à chaque tour"], ["souple", "outil appelé par le LLM"]]),
 ],
 pages=[
  dict(kicker="Chapitre 81 · voix", title="Pipecat et LiveKit Agents", sub="ne pas réécrire la plomberie", scene="trames", body="""
    <p class="lede">Un agent vocal, ce n’est pas seulement trois modèles : c’est du <b>son en flux</b>, des <b>tours de parole</b>, des <b>interruptions</b>, de l’<b>écho</b>. Deux cadres libres s’en chargent.</p>""" + L("<b>Pipecat</b> (Daily, licence BSD) : une bibliothèque Python où l’agent est une chaîne de processeurs.", "<b>LiveKit Agents</b> (LiveKit, licence Apache 2.0) : un cadre Python ou Node.js adossé au serveur WebRTC LiveKit.") + "<p>Ce chapitre prolonge le chapitre 80. Exemples vérifiés sur <b>Pipecat 1.15</b> et <b>LiveKit Agents 1.8</b> (novembre 2026) ; ces API changent vite.</p>"),
  dict(kicker="81.1", title="Pipecat : des trames", sub="le modèle mental", scene="trames", body=L("<b>Trames</b> : audio, transcription, texte, contexte, interruption, fin.", "<b>Processeurs</b> : chacun traite les trames qu’il comprend et transmet les autres.", "<b>Pipeline</b> : la liste ordonnée des processeurs ; <b>PipelineTask</b> l’exécute, <b>PipelineRunner</b> gère l’arrêt propre.", "<b>Interruption</b> : quand l’utilisateur parle, une trame d’interruption remonte et vide les files du LLM et du TTS.") + "<p>Écrire son propre processeur (filtre, RAG, journal) se fait en une vingtaine de lignes.</p>"),
  dict(kicker="81.2", title="Pipecat : un agent local", sub="micro, Whisper, Ollama, Piper", scene="hors", body=CODE("""ctx = LLMContext([{"role": "system", "content": PROMPT_ORAL}])
vad = SileroVADAnalyzer(params=VADParams(stop_secs=0.2))
agg = LLMContextAggregatorPair(ctx,
    user_params=LLMUserAggregatorParams(vad_analyzer=vad))
stt = WhisperSTTService(device="cuda",
    compute_type="int8_float16",
    settings=WhisperSTTService.Settings(
        model="large-v3-turbo", language=Language.FR,
        hotwords="Kyutai, Mimi"))
llm = OLLamaLLMService(
    settings=OLLamaLLMService.Settings(model="qwen3:8b"))
tts = PiperTTSService(
    settings=PiperTTSService.Settings(voice="fr_FR-siwis-medium"))
io = LocalAudioTransport(LocalAudioTransportParams(
    audio_in_enabled=True, audio_out_enabled=True))
pipeline = Pipeline([io.input(), stt, agg.user(), rag,
    llm, tts, io.output(), agg.assistant()])
task = PipelineTask(pipeline,
    params=PipelineParams(enable_metrics=True))
await PipelineRunner().run(task)""") + "<p>Imports omis. Dans un navigateur : <b>SmallWebRTCTransport</b>, sans serveur.</p>"),
  dict(kicker="81.3", title="Pipecat : régler les tours", sub="dans l’agrégateur utilisateur", scene="tours", body=L("<b>VAD</b> : <code>VADParams(confidence=0.7, start_secs=0.2, stop_secs=0.2, min_volume=0.6)</code> ; <code>stop_secs</code> court, car la fin de tour est confiée au modèle.", "<b>Fin de tour</b> : par défaut, <b>Smart Turn v3</b> (local, CPU) juge sur l’audio si la phrase est finie.", "<b>Stratégies</b> : <code>user_turn_strategies</code> pour changer les règles de début et de fin de tour.", "<b>Silence</b> : <code>user_turn_stop_timeout</code> (5 s par défaut) clôt un tour resté ouvert.", "<b>Mesures</b> : <code>enable_metrics=True</code> publie le délai de chaque service.")),
  dict(kicker="81.4", title="Pipecat : brancher le RAG", sub="un processeur avant le LLM", scene="rag", body=CODE("""class RAG(FrameProcessor):
    async def process_frame(self, frame, direction):
        await super().process_frame(frame, direction)
        if isinstance(frame, LLMContextFrame):
            msgs = frame.context.get_messages()
            question = msgs[-1]["content"]
            extraits = await chercher(question, k=3)
            frame.context.add_message({"role": "system",
                "content": "Extraits utiles :\\n" + extraits})
        await self.push_frame(frame, direction)""") + L("Ajouter les extraits <b>après</b> le prompt système stable, pour garder le cache.", "Retirer les extraits des tours précédents, sinon le contexte gonfle.", "Variante : <code>llm.register_function(\"chercher_notes\", ...)</code>, appelée par le LLM.")),
  dict(kicker="81.5", title="LiveKit : salles et sessions", sub="le modèle mental", scene="lkarchi", body=L("<b>Serveur LiveKit</b> : relaie l’audio et la vidéo entre participants d’une salle ; en local : <code>livekit-server --dev</code>.", "<b>AgentServer</b> : attend les demandes et lance un processus par conversation.", "<b>AgentSession</b> : les modèles (STT, LLM, TTS, VAD) et la gestion des tours.", "<b>Agent</b> : les consignes, les outils (<code>@function_tool</code>) et des crochets comme <code>on_user_turn_completed</code>.") + "<p>Test sans navigateur : <code>python agent.py console</code> parle directement par le micro et le haut-parleur du terminal.</p>"),
  dict(kicker="81.6", title="LiveKit : un agent local", sub="tout pointé vers des serveurs locaux", scene="hors", body=CODE("""VOIX = "http://localhost:8000/v1"   # Speaches
LLM = "http://localhost:11434/v1"   # Ollama
server = AgentServer()

@server.rtc_session()
async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=openai.STT(base_url=VOIX, language="fr",
            model="Systran/faster-whisper-large-v3"),
        llm=openai.LLM(base_url=LLM, model="qwen3:8b"),
        tts=openai.TTS(base_url=VOIX, model="kokoro",
            voice="ff_siwis"),
        turn_handling={"turn_detection": MultilingualModel()})
    await session.start(room=ctx.room, agent=Assistant())

agents.cli.run_app(server)""") + "<p>Ici, un serveur <b>Speaches</b> sur le port 8000 sert la reconnaissance et la synthèse, <b>Ollama</b> le LLM. Les noms de modèles dépendent de ce que vous y avez installé.</p>"),
  dict(kicker="81.7", title="LiveKit : régler les tours", sub="turn_handling", scene="tours", body=CODE("""turn_handling={
  "turn_detection": MultilingualModel(),
  "endpointing": {"min_delay": 0.4, "max_delay": 3.0},
  "interruption": {"min_duration": 0.5, "min_words": 2,
                   "resume_false_interruption": True},
  "preemptive_generation": {...},   # LLM lancé avant la fin sûre
}""") + L("<b>MultilingualModel</b> : modèle de fin de tour sur le texte, le français compris, exécuté en local.", "<b>min_delay</b> : silence minimum avant de répondre ; <b>max_delay</b> : attente maximale si le modèle pense que la phrase continue.", "<b>min_words</b> : n’interrompre l’agent que sur de vrais mots, pas sur un « mm ».")),
  dict(kicker="81.8", title="LiveKit : brancher le RAG", sub="un crochet avant chaque réponse", scene="rag", body=CODE("""class Assistant(Agent):
    def __init__(self):
        super().__init__(instructions=PROMPT_ORAL)

    async def on_user_turn_completed(self, turn_ctx, new_message):
        extraits = await chercher(new_message.text_content, k=3)
        turn_ctx.add_message(role="assistant",
            content="Informations utiles pour répondre : " + extraits)""") + "<p>Le crochet s’exécute à chaque tour, sans aller-retour du LLM. Les extraits ajoutés à <code>turn_ctx</code> ne valent que pour ce tour. Pour les recherches plus larges, ajouter une méthode <code>@function_tool</code> que le LLM appelle lui-même.</p>"),
  dict(kicker="81.9", title="Pipecat ou LiveKit ?", sub="selon l’usage", scene="compare", body=L("<b>Un assistant personnel sur une machine</b> : Pipecat, transport local ou SmallWebRTC. Un seul programme, aucun serveur à ajouter.", "<b>Un service pour plusieurs personnes</b>, sur le web ou au téléphone : LiveKit, qui répartit les conversations et gère la téléphonie SIP.", "<b>Contrôle fin du flux</b> (filtres, traductions, avatars) : Pipecat.", "<b>Transferts entre agents</b> (accueil, puis spécialiste) : les deux savent faire (Pipecat Flows, transferts d’Agent LiveKit).") + "<p>Pipecat sait aussi utiliser une salle LiveKit comme transport : les deux ne s’excluent pas.</p>"),
  dict(kicker="81.10", title="Pièges fréquents", sub="ce qui casse le naturel", scene="tours", body=L("<b>Écho</b> : sans annulation d’écho (navigateur, WebRTC) ni casque, l’agent s’entend et s’interrompt.", "<b>Deux détecteurs de fin de tour</b> superposés : délais qui s’additionnent.", "<b>Historique faux</b> après une interruption : vérifier que seule la partie prononcée est gardée (les deux cadres le font si le TTS fournit l’alignement).", "<b>Markdown lu à voix haute</b> : filtrer la sortie du LLM avant le TTS.", "<b>Premier appel lent</b> : précharger les modèles au démarrage.")),
  dict(kicker="81.11", title="Mesurer", sub="avant de régler", scene="trames", body=L("<b>Pipecat</b> : <code>enable_metrics=True</code> ; délai jusqu’au premier octet (TTFB) de chaque service, durée de traitement.", "<b>LiveKit</b> : événement <code>metrics_collected</code> : délai de fin de tour, premier jeton du LLM, premier son du TTS.", "<b>Bout en bout</b> : enregistrer des conversations réelles et mesurer de la fin de parole au premier son (médiane, percentile 95).") + "<p>Le tableau de correspondance des réglages et des défauts est au chapitre 80 (pages 80.10 à 80.15).</p>"),
 ],
 practice={1:[P("Dans Pipecat, comment une interruption arrête-t-elle la réponse en cours ?", ["une trame d’interruption vide les files du LLM et du TTS", "le programme redémarre", "le micro est coupé", "le LLM change de température"], 0, "Tout passe par des trames, y compris l’interruption.")],
           5:[P("Dans LiveKit Agents, que fait AgentServer ?", ["il attend les demandes et lance un processus par conversation", "il synthétise la voix", "il remplace le serveur WebRTC", "il entraîne le modèle"], 0, "Chaque conversation tourne dans son propre processus.")],
           9:[P("Pour un assistant vocal personnel sur un seul PC, hors ligne, quel choix est le plus simple ?", ["Pipecat avec un transport local", "LiveKit avec la téléphonie SIP", "un service en ligne", "aucun cadre"], 0, "Un seul programme, aucun serveur WebRTC à ajouter.")]}
)]
