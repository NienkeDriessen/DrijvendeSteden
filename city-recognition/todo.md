### TODOs voor Drijvende Steden project
# City Recognition
- Building_finder moet opgeschoond worden:
    - Voornamelijk documentatie
    - Parameters moeten uiteindelijk gefinetuned worden voor de telefoon die gebruikt gaat worden voor de foto's
- Grid_builder heeft nog een aantal problemen:
    - Alle coordinaten en de rotation worden berekend vanaf de anchor, wat betekend dat kleine afwijkingen (wat niet volledig te voorkomen is) een sterk effect kunnen hebben op punten die ver weg zitten van de anchor
    - De code zelf is redelijk ingewikkeld en slecht gedocumenteerd
- Building_recognizer herkent op dit moment alleen maar kleuren, dit zal voor de eerste versie waarschijnlijk zo blijven
- Color_recognizer moet getest worden voor verschillende foto's

# City viewer
Zo goed als af.

# Deployment - Dit werkt voor nu
Zo goed als af - Deploy op ScienceCentre accounts
- City recognition (PythonAnywhere)
- Storage (Google Firebase - Realtime Database)
- City viewer (Netlify)

### Misschien:
# City Editor
- Eventueel moet er misschien nog een city editor komen waarbij de tour guides wat missende gebouwtjes nog kunnen invullen
- Dit zou nog volledig uitgedacht moeten worden hoe dit zou werken
    - Eventueel tonen we alleen een grid en dan kunnen er gebouwtjes geplaatst worden op lege cellen
    - Soms kunnen bestaande gebouwtjes op de verkeerde plek staan, om ze dit te laten aanpassen kan misschien ook, maar is waarschijnlijk wel lastiger