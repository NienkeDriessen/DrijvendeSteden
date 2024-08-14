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
- Er moet nog een goede manier gevonden om de gebouwen in te lezen
    - Voor performance is het belangrijk dat elk verschillend gebouw maximaal 1 keer wordt ingelezen
    - Ideaal gezien is het niet een reeks van nested functies
    - Op dit moment wordt er overigens ook maar 1 gebouw ingelezen
- Het visuele gedeelte kan nog verbeterd worden, juiste kleuren/groote van gebouwen vinden etc

# Deployment - Dit werkt voor nu
- City recognition draait nu met een flask front-end in PythonAnywhere
- De stad definities worden opgeslagen in Google Firebase (Realtime Database)
- De city viewer runt op een simpele static website host (Netlify)

### Misschien:
# City Editor
- Eventueel moet er misschien nog een city editor komen waarbij de tour guides wat missende gebouwtjes nog kunnen invullen
- Dit zou nog volledig uitgedacht moeten worden hoe dit zou werken
    - Eventueel tonen we alleen een grid en dan kunnen er gebouwtjes geplaatst worden op lege cellen
    - Soms kunnen bestaande gebouwtjes op de verkeerde plek staan, om ze dit te laten aanpassen kan misschien ook, maar is waarschijnlijk wel lastiger