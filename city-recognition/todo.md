### TODOs voor Drijvende Steden project
# City Recognition
- Building_finder moet opgeschoond worden:
    - Voornamelijk documentatie
    - Parameters moeten uiteindelijk gefinetuned worden voor de telefoon die gebruikt gaat worden voor de foto's
- Grid_builder heeft nog een aantal problemen:
    - x en y lijken oppeens omgedraaid te worden voor height en width (en de rest van de code is hier op aangepast), alles moet even nagekeken worden wat de juiste manier moet zijn
    - Alle coordinaten en de rotation worden berekend vanaf de anchor, wat betekend dat kleine afwijkingen (wat niet volledig te voorkomen is) een sterk effect kunnen hebben op punten die ver weg zitten van de anchor
    - De code zelf is redelijk ingewikkeld en slecht gedocumenteerd
- Building_recognizer herkent op dit moment alleen maar kleuren, dit zal voor de eerste versie waarschijnlijk zo blijven
- Color_recognizer moet getest worden voor verschillende foto's

# City Editor
- Eventueel moet er misschien nog een city editor komen waarbij de tour guides wat missende gebouwtjes nog kunnen invullen
- Dit zou nog volledig uitgedacht moeten worden hoe dit zou werken
    - Eventueel tonen we alleen een grid en dan kunnen er gebouwtjes geplaatst worden op lege cellen
    - Soms kunnen bestaande gebouwtjes op de verkeerde plek staan, om ze dit te laten aanpassen kan misschien ook, maar is waarschijnlijk wel lastiger


# City viewer
- Er moet nog een goede manier gevonden om de gebouwen in te lezen
    - Voor performance is het belangrijk dat elk verschillend gebouw maximaal 1 keer wordt ingelezen
    - Ideaal gezien is het niet een reeks van nested functies
    - Op dit moment wordt er overigens ook maar 1 gebouw ingelezen
- Het visuele gedeelte kan nog verbeterd worden, juiste kleuren/groote van gebouwen vinden etc

# Deployment
- Dit moet grotendeels nog uitgezocht worden
- City recognition (en editor)
    - De city recognition moet ergens runnen (er kan getest worden of dit direct op de telefoon kan, anders moet dit waarschijnlijk ergens op een server runnen)
    - Als het extern wordt gerunt dan moet er nog iets van een interface zijn waarin de foto aangeleverd kan worden aan de server (misschien kan dit wel via een bestaande messaging app - discord, whatsapp, email etc) - Goede kwaliteit foto is wel belangrijk, dus services met heftige compressie zijn misschien niet geschikt.
    - Voor de city editor hangt het er erg van af hoe het wordt geimplementeerd en hoe de city recognition wordt deployed
- City viewer
    - Dit moet gewoon ergens gehost worden, waarschijnlijk geen backend nodig
    - Hoe we precies een ander domein naam koppelen bij de hosting service die we gebruiken moet nog uitgezocht worden
    - Ook moeten we nog uitzoeken hoe we de definities van de stad opslaan en accessen
        - Het handigste is waarschijnlijk als we de definities ergens opslaan met een ID, en dan deze ID meegeven in de URL als parameter